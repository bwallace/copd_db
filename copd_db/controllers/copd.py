import logging
import pdb
import time
from copd_db.lib.base import *
from copd_db.model import meta
from copd_db.model.meta import Association, Gene, Arm, Publication, Demographic
from copd_db.lib import meta_py_r
from sqlalchemy import orm
from sqlalchemy import and_
from sqlalchemy import *
import decimal


log = logging.getLogger(__name__)

# Some meta data for numerical encodings in the database.
# TODO these should be stored as a tables in the SQL db    
_race_encodings = {"1": "European", "2":"Asian", "3":"African", "4":"Indian", "5":"Other", "":""}
_emph_encodings = {1:"CT", 2:"Chest X-Ray", 3:"Pathology", "":""}
    
class CopdController(BaseController):
    '''
    This is the main controller module of the COPDdb application. It handles client requests, as specified per routes.py, 
    and dispatches appropriately.
    '''

    def index(self):
        # fetch all associations... 
        associations_q = meta.Session.query(Association)
        genes_q = meta.Session.query(Gene)
        c.currently_selected_gene = None
        c.all_genes = genes_q.all()
        c.currently_selected_polymorphism = None
        c.associations = associations_q.all()
	    # ... and render them
        return render("/index.mako")

    def gene_selected(self):
        ''' When a gene is selected, we refresh the polymorphism drop-down '''
        selected_gene = request.params['GeneName']
        c.currently_selected_gene = selected_gene
        
        # get the gene object associated with this name
        gene_q = meta.Session.query(Gene)
        c.currently_selected_gene = gene_q.filter(Gene.gene_name == selected_gene).all()[0]
        
        # now pull the corresponding associations
        associations_q = meta.Session.query(Association)
        c.associations = associations_q.filter(Association.gene_id ==  c.currently_selected_gene.id).all()
        # the polymorphism fragment also needs to know the gene name
        c.gene_name = selected_gene
        return render("/polymorphism_fragment.mako")
        
    def update_displayed_data(self):
        if request.params['DisplayThis'] == "demographics":
            c.table = _make_demographics_data_table(session["demographics"], session["publications"])
        else:
            c.table = _make_study_data_table(session["data_used"], session["publications"])
        return render("/table_fragment.mako")
    
    def _waiting(self):
        print "\n YLDJFKJF"
        def wait_pause():
            #pdb.set_trace()
            done = False
            #pdb.set_trace()
            while not done:
                print "??"
                c.img_path =  "/images/loading.gif"
                yield render("/waiting.mako")
                done = True
                print "waiting..."
                time.sleep(10)
        return wait_pause()

            
    def polymorphism_selected(self):
        ''' 
        When a polymorphism is selected, we need to run the analysis over the associated 
        studies and then render the results. This routine is responsibile for doing this.
        '''
        selected_polymorphism = request.params['Polymorphism']
        
    
        if selected_polymorphism == "":
            return "No polymorphism selected."
            
        #pdb.set_trace()
        #self._waiting()
        print "starting"

        selected_gene = request.params['Gene']
        
        ma_results, demographics, pub_info = self._run_ma_for_gene_poly(selected_gene, selected_polymorphism)
        
        # unpack results
        r_results = ma_results[0]
        c.img_path = r_results[0]
        #
        # The following two fields are `cached' using the session
        # global dict, so that the user can select which table is 
        # displayed after the fact
        #
        session["data_used"] =  ma_results[1]
        session["demographics"] = demographics
        session["publications"] = pub_info
        session.save()

        # we default to the data used table
        print "done"
        c.table = _make_study_data_table(session["data_used"], session["publications"])
        return render("/results_fragment.mako")

    def _run_ma_for_gene_poly(self, selected_gene, selected_polymorphism):
        genes_q = meta.Session.query(Gene)
        gene = genes_q.filter(Gene.gene_name == selected_gene).one()
        
        # get all the associations for this gene/polymorphism pair
        associations_q = meta.Session.query(Association)
        associations = associations_q.filter(and_(Association.gene_id == gene.id, Association.polymorphism == selected_polymorphism)).all()
        # the ids of the associations that match this gene/poly
        association_ids = [assoc.id for assoc in associations]
        
        # figure out which publications these associations map to
        arm_q = meta.Session.query(Arm)
        all_publication_ids = set([arm_q.filter(Arm.id == association.group_id).one().study_id for association in associations])
        
        publications_q = meta.Session.query(Publication)
        demographics_q = meta.Session.query(Demographic)
        
        # now build 'analysis unit' objects using the retrieved publications
        analysis_units, demographics, pub_info = [], [], []
        for publication_id in all_publication_ids:
            try:
                # fetch publication info
                cur_pub = publications_q.filter(Publication.id == publication_id).one()
                
                # fetch all control arms associated with this publication
                control_arms = arm_q.filter(and_(Arm.study_id == publication_id, Arm.is_control == True)).all()
                control_associations = [associations_q.filter(Association.group_id == control_arm.id).one() for control_arm in control_arms]
                # now filter to make sure the association maps to this gene/polymorphism pair
                control_associations = [assoc for assoc in control_associations if assoc.id in association_ids]
                
                # wash and repeat for case
                case_arms = arm_q.filter(and_(Arm.study_id == publication_id, Arm.is_control == False)).all()
                case_associations = [associations_q.filter(Association.group_id == case_arm.id).one() for case_arm in case_arms]
                case_associations = [assoc for assoc in case_associations if assoc.id in association_ids]
                
                for control_association, case_association in zip(control_associations, case_associations):
                    pub_info.append(cur_pub)
                    is_car = control_association.is_car
                    # build the analysis unit object
                    analysis_units.append(meta_py_r.AnalysisUnit(case_association, control_association,
                                                                                            cur_pub, is_car))
                    case_arm_demos = demographics_q.filter(Demographic.group_id == case_association.group_id).one()
                    control_arm_demos =  demographics_q.filter(Demographic.group_id == control_association.group_id).one()
                    demographics.append({"case":case_arm_demos,  "control":control_arm_demos})                                                                                          
                                                                                     
            except Exception, inst:
                print inst
                return "sorry... there was an error. here's the trace: %s" % inst
            
        ma_results = meta_py_r.run_analysis_with_units(analysis_units)
        return (ma_results, demographics, pub_info)

def _make_study_data_table(data, publications, headers = ["study", "year", "cases", "controls", "cases A", "cases B", "controls A", "controls B"], 
                                                    cols = ["study", "year", "n.e", "n.c", "case_as", "case_bs", "control_as", "control_bs"]):
    ''' builds and returns a table with the study data for the parametric studies '''
    table = _add_headers([], ["", "people", "alleles"], spans = [2, 2, 4])
    table = _add_headers(table, headers)
    
    for study_index in range(len(data["study"])):
        table.append("<tr>")
        
        for col in cols:
            cur_cell_val = data[col][study_index]
            #pdb.set_trace()
            #cur_cell_val = str(cur_cell_val.to_integral()) if isinstance(cur_cell_val, decimal.Decimal) else cur_cell_val
            
            
            if col in ["n.e", "n.c"] and not data["car_flags"][study_index]:
                cur_float_val = float(cur_cell_val)/2.0
                cur_cell_val = _num_to_pretty_str(cur_float_val)
            elif col in ["case_as", "case_bs", "control_as", "control_bs"]:
                cur_cell_val = _num_to_pretty_str(cur_cell_val)
                
            # if it's the study column, include a link to the pubmed article
            if col == "study":
                table.append(
                    "<td><a href = http://www.ncbi.nlm.nih.gov/sites/entrez?db=pubmed&cmd=search&term=%s target='_blank'>%s</a></td>" % 
                    (publications[study_index].pubmed_id, cur_cell_val))
            else:
                table.append("<td>%s</td>" % cur_cell_val)
        table.append("</tr>")
        

    return " ".join(table)

def _num_to_pretty_str(x):
    if x == int(x):
        return str(int(x))
    else:
        return str(x)
    	    
def _make_demographics_data_table(demographics, publications):
    ''' 
    This method assembles and returns the (html) table for the parametric demographics object. It 
    does not include the <table> and </table> tags, however, as we expect the table_fragment
    template to do this for us.
    '''
    # first head is blank to account for the study column
    control_headers = ["race", "% male", "mean age", "avg. pack-years"]
    case_headers = list(control_headers)

    control_span = len(control_headers)
    cases_span = len(case_headers)
    
    table = _add_headers([], ["study", "controls", "cases"], spans=[1, control_span, cases_span])      
    control_headers.insert(0, "") # for study column
    control_headers.extend(case_headers)
    table = _add_headers(table, control_headers)
    
    for i, demographic in enumerate(demographics):
        table.append("<tr>")
        
        # first append the study name
        table.append(
            "<td><a href = http://www.ncbi.nlm.nih.gov/sites/entrez?db=pubmed&cmd=search&term=%s target='_blank'>%s</a></td>" % 
            (publications[i].pubmed_id, publications[i].author))
        
        cont_d = demographic["control"]
        perc_males = cont_d.perc_male_controls
        if isinstance(perc_males, float):
            perc_males = round(perc_males)
        else:
            perc_males = perc_males.to_integral() if cont_d.perc_male_controls is not None else None
            
        race_val = _race_encodings[cont_d.race] if cont_d.race is not None else ""
        cont_vals = [race_val,  perc_males,
                              cont_d.mean_age_controls, 
                              cont_d.mean_pack_years_controls]
        cont_vals = [_process_str(s) for s in cont_vals]

        table.append("<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % tuple(cont_vals)) 
        
        # case fields
        case_d = demographic["case"]
        emph = ""
        try:
            emph = _emph_encodings[case_d.emphysema]
        except:
            pass
         
        perc_males = case_d.perc_male_cases
        if isinstance(perc_males, float):
            perc_males = round(perc_males)
        else:  
            perc_males = perc_males.to_integral() if case_d.perc_male_cases is not None else None
            
        race_val = _race_encodings[case_d.race] if case_d.race is not None else ""
        case_vals = [race_val,  perc_males,
                            case_d.mean_age_cases,
                            case_d.mean_pack_years_cases]
        case_vals = [_process_str(s) for s in case_vals]         
        table.append("<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" %
                              tuple(case_vals)) 
                                                                                  

        table.append("</tr>")
    
    return " ".join(table)
    

def _count_non_nones(ls):
    count = 0
    for x in ls:
        if x is not None:
            count+=1
    return count    

def _process_str(x):
    if x is None:
        return ""
    
    if x < 0:
        return "N/A"

    return x
    
def _add_headers(table, headers, spans = None):
    if spans is None:
        spans = [1 for header in headers]
    table.append("<tr>")
    for span, header in zip(spans, headers):
    	table.append("<th colspan='%s'>%s</th>" % (span, header))
    table.append("</tr>")
    return table
    
def _arg_max(ls, f):
    ''' Returns the element x in ls for which f(x) is greatest. '''
    cur_max = f(ls[0])
    rval = ls[0]
    for x in ls[1:]:
        cur_val = f(x)
        if cur_val > cur_max:
            rval = x
            cur_max =cur_val
    return rval