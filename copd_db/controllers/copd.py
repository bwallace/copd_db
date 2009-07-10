import logging
import pdb
from copd_db.lib.base import *
from copd_db.model import meta
from copd_db.model.meta import Association, Gene, Arm, Publication, Demographic
from copd_db.lib import meta_py_r
from sqlalchemy import orm
from sqlalchemy import and_
from sqlalchemy import *

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
            c.table = _make_demographics_data_table(session["demographics"])
        else:
            c.table = _make_study_data_table(session["data_used"])
        return render("/table_fragment.mako")
    
    
    def polymorphism_selected(self):
        ''' 
        When a polymorphism is selected, we need to run the analysis over the associated 
        studies and then render the results. This routine is responsibile for doing this.
        '''
        selected_polymorphism = request.params['Polymorphism']

        print selected_polymorphism
    
        if selected_polymorphism == "":
            return "No polymorphism selected."
            
        selected_gene = request.params['Gene']
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
        analysis_units, demographics = [], []
        for publication_id in all_publication_ids:
            try:
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
                    # build the analysis unit object
                    analysis_units.append(meta_py_r.AnalysisUnit(case_association, control_association,
                                                                                            publications_q.filter(Publication.id == publication_id).one()))
                    case_arm_demos = demographics_q.filter(Demographic.group_id == case_association.group_id).one()
                    control_arm_demos =  demographics_q.filter(Demographic.group_id == control_association.group_id).one()
                    demographics.append({"case":case_arm_demos,  "control":control_arm_demos})                                                                                          
                                                                                     
            except Exception, inst:
                print inst
                return "sorry... there was an error. here's the trace: %s" % inst
            
        ma_results = meta_py_r.run_analysis_with_units(analysis_units)
        # unpack results
        r_results = ma_results[0]
        c.img_path = r_results[0]
        #
        # The following two fields are `cached' so that
        # the user can select which table is displayed after the fact
        #
        session["data_used"] =  ma_results[1]
        session["demographics"] = demographics
        session.save()

        # we default to the data used table
        c.table = _make_study_data_table(session["data_used"])
        return render("/results_fragment.mako")


def _make_study_data_table(data, headers = ["study", "year", "num. cases", "num. controls"], cols = ["study", "year", "n.e", "n.c"]):
    ''' builds and returns a table with the study data for the parametric studies '''
    table = _add_headers([], headers)
    for study_index in range(len(data["study"])):
        table.append("<tr>")
        for col in cols:
            cur_cell_val = data[col][study_index]
            if study_index in ["n.e", "n.c"]:
                cur_cell_val = str(float(cur_cell_val / 2.0))
            table.append("<td>%s</td>" % cur_cell_val)
        table.append("</tr>")
        

    return " ".join(table)

    	    
def _make_demographics_data_table(demographics):

    control_headers = ["race", "% male", "mean age", "avg. pack-years"]
    case_headers = list(control_headers)
    case_headers.extend(["phenotype", "emphysema" ])

    control_span = len(control_headers)#_count_non_nones(demographics["controls"])
    cases_span = len(case_headers)#_count_non_nones(demographics["cases"])
    
    table = _add_headers([], ["controls", "cases"], spans=[control_span, cases_span])      
    control_headers.extend(case_headers)
    table = _add_headers(table, control_headers)
    
    for demographic in demographics:
        table.append("<tr>")
        cont_d = demographic["control"]
        cont_vals = [_race_encodings[cont_d.race],  cont_d.perc_male_controls,
                              cont_d.mean_age_controls, 
                              cont_d.mean_pack_years_controls]
        cont_vals = [_none_to_str(s) for s in cont_vals]

        table.append("<td>%s</td><td>%s</td><td>%s</td><td>%s</td>" % tuple(cont_vals)) 
        
        # case fields
        case_d = demographic["case"]
        emph = ""
        try:
            emph = _emph_encodings[case_d.emphysema]
        except:
            pass
            
        case_vals = [_race_encodings[case_d.race],  case_d.perc_male_cases,
                            case_d.mean_age_cases,
                            case_d.mean_pack_years_cases,
                            case_d.copd_phenotype,
                            emph]
        case_vals = [_none_to_str(s) for s in case_vals]         
        table.append("<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>" %
                              tuple(case_vals)) 
                                                                                  

        table.append("</tr>")
    
    return " ".join(table)
    
def _count_non_nones(ls):
    count = 0
    for x in ls:
        if x is not None:
            count+=1
    return count    
        
def _none_to_str(x):
    if x is None:
        return ""
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