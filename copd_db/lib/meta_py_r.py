'''
This module is a bridge from python to R for conducting meta-analyses. Uses rpy2.
'''

import pdb
import os
import time
import rpy2
from rpy2 import robjects as ro

#
# Here we tell R to load the requisite libraries
#
ro.r("library(meta)")
ro.r("library(Cairo)")

class AnalysisUnit(object):
    '''
    This is a composite class for representing the unit of analysis for meta-analyses; comprised
    of the case and control group, as well as the study these were pulled from.
    '''
    def __init__(self, case_association, control_association, study, label = None):
        self.case_association = case_association
        self.control_association = control_association 
        self.study = study
        self.label = label if label is not None else study.author
        
        
def run_analysis_with_units(analysis_units):
    dataf, data_used_in_ma = units_to_r_data_frame(analysis_units)
    # these encode the label for the respective alleles -- we need them
    # for the forest plot label.
    a_str = analysis_units[0].control_association.a_string
    b_str = analysis_units[0].control_association.b_string
    # the former points to the analysis results, as per R, and the latter is a dictionary
    # with the data used in the analysis.
    return (run_analysis(dataf, a_str, b_str), data_used_in_ma)
    
def units_to_r_data_frame(analysis_units):
    case_events, case_totals, control_events, control_totals, labels, years = [], [], [], [], [], []
    for analysis_unit in analysis_units:
        # we're assuming a is the 'event' -- arbitrarily
        case_events.append(analysis_unit.case_association.a)
        case_totals.append(analysis_unit.case_association.a + analysis_unit.case_association.b)
        control_events.append(analysis_unit.control_association.a)
        control_totals.append(analysis_unit.control_association.a + analysis_unit.control_association.b)
        labels.append(analysis_unit.label)
        years.append(analysis_unit.study.pub_date)

    # now build a dictionary from the assembled data that will be used to make an r frame
    d = {"study": ro.StrVector(labels), "year":ro.IntVector(years), "event.e":ro.FloatVector(case_events), "n.e":ro.FloatVector(case_totals), 
                                                                                                  "event.c":ro.FloatVector(control_events), "n.c":ro.FloatVector(control_totals)}
    print "case events: %s\n, case totals: %s\n, control events: %s\n, control totals: %s\n" %(case_events, case_totals, control_events, control_totals)
    
    # this is just to make life easier on the python end -- rather than dealing with the R objects we return another python dictionary
    # with the data used in the analysis
    data_for_py = {"study": labels, "year":years, "event.e":case_events, "n.e":case_totals, 
                                                                      "event.c":control_events, "n.c":control_totals}
    # next cast this to a frame
    dataf = ro.r['data.frame'](**d)

    
    # return a tuple, with both the R object and the python dictionary -- we need the latter to render the 
    # data to the user
    return (dataf, data_for_py)
    
def run_analysis(r_frame, a_str, b_str):
    plot_name = str(time.time()) + ".png"
    my_result = None
    try:
        my_result = ro.r('metabin(event.e, n.e, event.c, n.c, data=%s, studlab=paste(study, paste("(", year, ")", sep=""), sep=" "), sm="OR")' % r_frame.r_repr())
        
        # write the image to the public directory, under 'results', using the current timestamp as a filename
        path = os.getcwd().split(os.path.sep)[:-1]
        path.extend(["copd_db", "copd_db", "public", "results", plot_name])
        path = os.path.sep.join(path)
        ro.r.CairoPNG(path, height=300, width=800)
        ro.r('forest(%s, lab.e = "Cases", lab.c ="Controls", leftlabs = c("%s", "%s", "%s", "%s", "%s"), rightcols = c("effect", "ci"), comb.random=TRUE)' % (my_result.r_repr(), "Study", a_str, b_str, a_str, b_str))
        ro.r['dev.off']()
        pdb.set_trace()
        print "CHANGE THIS PATH BEFORE DEPLOYING"
        img_path = "/results/%s" % plot_name
        #img_path = "/copddb/results/%s" % plot_name
    except Exception, inst:
        print "whoops. problem running analysis:\n %s" % inst
        print "returning None tuple..."
        img_path = None

    return (img_path, my_result) 
    
    
    
def associations_to_r_data_frame(associations):
    tx_events, tx_total, control_events, control_total = [], [], [], [], [] , []
    for association in associations:
        tx_events.append()
    
def dummy_analysis():    
    ''' Simple hard-coded example '''
    
    d = {"study": ro.StrVector(('byron', 'tom')), "year":ro.IntVector((1999, 2000)), "event.e": ro.IntVector((10, 20)), "n.e":ro.IntVector((100,200)), "event.c":ro.IntVector((13,22)), "n.c":ro.IntVector((100, 150))}
     
    dataf = ro.r['data.frame'](**d)
    
    plot_name = str(time.time())
    
    myresult = ro.r('metabin(event.e, n.e, event.c, n.c, data=%s, studlab=paste(study, paste("(", year, ")", sep=""), sep=" "))' % dataf.r_repr())
    path = os.getcwd().split(os.path.sep)[:-1]
    path.extend(["copd_db", "copd_db", "public", "results", plot_name])
    path = os.path.sep.join(path)

    ro.r.png(path,width=800,height=400)
    ro.r("forest(%s)" % myresult.r_repr())
    ro.r['dev.off']()

    img_path = "/results/%s" % plot_name
    return (img_path, myresult)
    

        
    