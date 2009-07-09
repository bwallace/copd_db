import logging
import pdb
from copd_db.lib.base import *
from copd_db.model import meta
from copd_db.model.meta import Association
from copd_db.model.meta import Gene
from copd_db.model.meta import Arm
from copd_db.model.meta import Publication
from copd_db.lib import meta_py_r
from sqlalchemy import orm
from sqlalchemy import and_

log = logging.getLogger(__name__)

class CopdController(BaseController):

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
        ''' When a geene is selected, we refresh the polymorphism drop-down '''
        selected_gene = request.params['GeneName']
        c.currently_selected_gene = selected_gene
        
        # get the gene object associated with this name
        gene_q = meta.Session.query(Gene)
        c.currently_selected_gene = gene_q.filter(Gene.gene_name == selected_gene).all()[0]
        
        # now pull the corresponding associations
        associations_q = meta.Session.query(Association)
        c.associations = associations_q.filter(Association.gene_id ==  c.currently_selected_gene.id).all()
        # the polymorphism fragment also needs to know the gene name. 
        # note: should this go in the globals (g) ?
        c.gene_name = selected_gene
        return render("/polymorphism_fragment.mako")
        
    def polymorphism_selected(self):
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

        # now build 'analysis unit' objects using the 
        analysis_units = []
       
      #  size_of_association = lambda(association): association.a + association.b
        for publication_id in all_publication_ids:
            try:
                control_arms = arm_q.filter(and_(Arm.study_id == publication_id, Arm.is_control == True)).all()
                control_associations = [associations_q.filter(Association.group_id == control_arm.id).one() for control_arm in control_arms]
                # now filter to make sure the association maps to this gene/polymorphism pair
                control_associations = [assoc for assoc in control_associations if assoc.id in association_ids]
                
                case_arms = arm_q.filter(and_(Arm.study_id == publication_id, Arm.is_control == False)).all()
                case_associations = [associations_q.filter(Association.group_id == case_arm.id).one() for case_arm in case_arms]
                case_associations = [assoc for assoc in case_associations if assoc.id in association_ids]
                
                for control_association, case_association in zip(control_associations, case_associations):
                    # build the analysis unit object
                    analysis_units.append(meta_py_r.AnalysisUnit(case_association, control_association,
                                                                                                                        publications_q.filter(Publication.id == publication_id).one()))
                                                                                                                
                                                                                     
            except Exception, inst:
                print inst
                return "sorry... there was an error. here's the trace: %s" % inst
            
        ma_results = meta_py_r.run_analysis_with_units(analysis_units)
        r_results = ma_results[0]
        c.img_path = r_results[0]
        c.data_used = ma_results[1]
        
        return render("/results_fragment.mako")

def _arg_max(ls, f):
    ''' Returns the element in ls for which f(ls) is greatest. '''
    cur_max = f(ls[0])
    rval = ls[0]
    for x in ls[1:]:
        cur_val = f(x)
        if cur_val > cur_max:
            rval = x
            cur_max =cur_val
    return rval