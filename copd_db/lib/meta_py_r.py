'''
This module is a bridge from python to R for conducting meta-analyses. Uses rpy2.
'''
from __future__ import with_statement

import pdb
import os
import time
import rpy2
from rpy2 import robjects as ro
import gc
import os, cPickle
import math




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
    def __init__(self, case_association, control_association, study, is_car, label = None):
        self.case_association = case_association
        self.control_association = control_association
        self.is_car = is_car
        self.study = study
        self.label = label if label is not None else study.author


def run_in_separate_process(func, *args, **kwds):
    pread, pwrite = os.pipe()
    pid = os.fork()
    if pid > 0:
        os.close(pwrite)
        with os.fdopen(pread, 'rb') as f:
            status, result = cPickle.load(f)
        os.waitpid(pid, 0)
        if status == 0:
            return result
        else:
            raise result
    else:
        os.close(pread)
        try:
            result = func(*args, **kwds)
            status = 0
        except Exception, exc:
            result = exc
            status = 1
        with os.fdopen(pwrite, 'wb') as f:
            try:
                cPickle.dump((status,result), f, cPickle.HIGHEST_PROTOCOL)
            except cPickle.PicklingError, exc:
                cPickle.dump((2,exc), f, cPickle.HIGHEST_PROTOCOL)
        os._exit(0)


def run_analysis_with_units(analysis_units):
    dataf, data_used_in_ma = units_to_r_data_frame(analysis_units)
    # these encode the label for the respective alleles -- we need them
    # for the forest plot label.
    a_str = analysis_units[0].control_association.a_string
    b_str = analysis_units[0].control_association.b_string
    # the former points to the analysis results, as per R, and the latter is a dictionary
    # with the data used in the analysis.
    #r_results = run_in_separate_process(run_analysis, dataf, a_str, b_str)
    return_tuple = (run_analysis(dataf, a_str, b_str, data_used_in_ma), data_used_in_ma)
    #return_tuple = (r_results, data_used_in_ma)
    # clear R objects
    print "clearing..."
    ro.r("rm(list=ls())")
    gc.collect()
    return return_tuple

def units_to_r_data_frame(analysis_units):
    case_events, case_as, case_bs, case_totals = [], [], [], []
    control_events, control_as, control_bs, control_totals = [], [], [], []
    labels, years = [], []
    car_flags = []
    for analysis_unit in analysis_units:
        # we're assuming a is the 'event' -- arbitrarily
        case_events.append(analysis_unit.case_association.a)
        case_totals.append(analysis_unit.case_association.a + analysis_unit.case_association.b)
        control_events.append(analysis_unit.control_association.a)
        control_totals.append(analysis_unit.control_association.a + analysis_unit.control_association.b)
        labels.append(analysis_unit.label.split(";")[0])
        # this is redundant, but makes life easier, and hopefully clearer, than using the _events as a, etc
        case_as.append(analysis_unit.case_association.a)
        case_bs.append(analysis_unit.case_association.b)
        control_as.append(analysis_unit.control_association.a)
        control_bs.append(analysis_unit.control_association.b)

        car_flags.append(analysis_unit.is_car)
        years.append(analysis_unit.study.pub_date)

    # now build a dictionary from the assembled data that will be used to make an r frame


    #d = {"study": ro.StrVector(labels), "year":ro.IntVector(years), "event.e":ro.FloatVector(floats_to_ints(case_events)),
    #                    "n.e":ro.FloatVector(floats_to_ints(case_totals)),  "event.c":ro.FloatVector(floats_to_ints(control_events)),
    #                     "n.c":ro.FloatVector(floats_to_ints(control_totals))}
    lors, std_errors, include_these = zero_cell_correct(case_events, case_totals, control_events, control_totals)

    d = {"study": ro.StrVector(labels), "year":ro.IntVector(years), "event.e":ro.FloatVector(floats_to_ints(case_events)),
                        "n.e":ro.FloatVector(floats_to_ints(case_totals)),  "event.c":ro.FloatVector(floats_to_ints(control_events)),
                        "n.c":ro.FloatVector(floats_to_ints(control_totals)), "TE":ro.FloatVector(lors),
                        "seTE":ro.FloatVector(std_errors), "subset":ro.BoolVector(include_these)}


    print "case events: %s\n, case totals: %s\n, control events: %s\n, control totals: %s\n" %\
                        (case_events, case_totals, control_events, control_totals)

    # this is just to make life easier on the python end -- rather than dealing with the R objects we return another python dictionary
    # with the data used in the analysis
    data_for_py = {"study": labels, "year":years,
                            "event.e":case_events, "n.e":case_totals, "case_as":case_as, "case_bs":case_bs,
                            "event.c":control_events, "n.c":control_totals, "control_as":control_as, "control_bs":control_bs,
                            "car_flags":car_flags, "test":ro.StrVector(["hi" for x in include_these])}
    # next cast this to a frame
    dataf = ro.r['data.frame'](**d)


    # return a tuple, with both the R object and the python dictionary -- we need the latter to render the
    # data to the user
    return (dataf, data_for_py)



def add_const(case_event, case_total, control_event, control_total, const=.5):
    values = [case_event, case_total, control_event, control_total]
    check = lambda x,y: x == y or x == 0
    if check(case_event, case_total) and check(control_event, control_total):
       return None
    elif check(case_event, case_total) or check(control_event, control_total):
       return cont_correction_method(values)
    return values

def zero_cell_correct(case_events, case_totals, control_events, control_totals, \
                                   cont_correction_method=add_const):
    # computes continuity-corrected values for OR calculations
    log_ors, std_errors = [], []
    include_studies = []
    for i in range(len(case_events)):
        corrected_vals = cont_correction_method(case_events[i], case_totals[i],\
                                                control_events[i], control_totals[i])
        if corrected_vals is None:
            log_ors.append(None)
            std_errors.append(None)
            include_studies.append(False)
        else:
            numerator = math.log(corrected_vals[0]/(corrected_vals[1] - corrected_vals[0]))
            denom = math.log(corrected_vals[2]/(corrected_vals[3] - corrected_vals[2]))
            log_ors.append(numerator- denom)
            std_errors.append(sum([1/x for x in corrected_vals]))
            include_studies.append(True)

    return [log_ors, std_errors, include_studies]




def floats_to_ints(ls):
    int_ls = []
    for x in ls:
        try:
            int_ls.append(int(str(x)))
        except:
            float_val = float(str(x))
            if float_val == round(float_val):
                int_ls.append(int(float_val))
            else:
                int_ls.append(float_val)
    return int_ls

def run_analysis(r_frame, a_str, b_str, pydata):

    plot_name = str(time.time()) + ".png"
    my_result = None
    try:
        #my_result = ro.r('metabin(event.e, n.e, event.c, n.c, data=%s, studlab=paste(study, paste("(", year, ")", sep=""), sep=" "), sm="OR")' %\
        #                  r_frame.r_repr())
        pdb.set_trace()
        my_result = ro.r('metagen(TE, seTE, data=%s, subset=subset, lbl.cols=test,   \
                          studlab=paste(study, paste("(", year, ")", sep=""), sep=" "), sm="OR")' %\
                          r_frame.r_repr())


        #ro.r('tmp_res<-metagen(TE, seTE, data=%s, subset=subset, \
        #                  studlab=paste(study, paste("(", year, ")", sep=""), sep=" "), sm="OR")' %\
        #                  r_frame.r_repr())



        #pdb.set_trace()
        #ro.r('class(%s) <- c("metagen", "meta")' %  my_result.r_repr())

        # write the image to the public directory, under 'results', using the current timestamp as a filename
        path = os.getcwd().split(os.path.sep)[:-1]
        path.extend(["copd_db", "copd_db", "public", "results", plot_name])
        path = os.path.sep.join(path)

        scaled_h = 350 + r_frame.nrow() * 7
        # change to CairoPDF if you want a PDF
        ro.r.CairoPNG(path, height=scaled_h, width=820)
        #ro.r.CairoPDF(path, height = 7, width= 9)


        pdb.set_trace()

        ro.r('forest(as(%s, "meta"), lab.e = "Cases", lab.c ="Controls", leftlabs = c("%s", "%s", "%s", "%s", "%s"),\
                               rightcols = c("effect", "ci"), leftcols=pydata["test"], comb.fixed=FALSE, comb.random=TRUE)' % \
                               (my_result.r_repr(), "Study", a_str, a_str + "+" + b_str, a_str, a_str + "+" + b_str))
        #ro.r('forest(%s, leftcols = c("studlab"), rightcols = c("effect", "ci"), comb.random=TRUE)' % (my_result.r_repr()))
        ro.r['dev.off']()
        #pdb.set_trace()
        #print "CHANGE THIS PATH BEFORE DEPLOYING"
        img_path = "/results/%s" % plot_name
        #img_path = "/copddb/results/%s" % plot_name # for webfaction
    except Exception, inst:
        print "whoops. problem running analysis:\n %s" % inst
        print "returning None tuple..."
        img_path = None

    return (img_path, my_result)

def _rls_to_pyd(r_ls):
    # base case is that the type is a native python type, rather
    # than an Rvector
    d = {}

    for name, val in zip(r_ls.getnames(), r_ls):
        try:
            # first check the key
            if str(name) != "NULL":
                print name
                print type(name)
                if "rpy2.robjects" in str(type(name)):
                    name = str(name[0])
                if not "rpy2.robjects" in str(type(val)):
                    # base case; not an rtype object
                    d[name] = val
                elif str(val)=="NULL":
                    d[name] = None
                elif str(val.getnames())=="NULL":
                    d[name] = val[0]
                else:
                    d[name] = _rls_to_pyd(val)
                if not isinstance(name, str):
                    raise Exception, "arg"
            else:
                # name is null
                return val

        except Exception,  inst:
            print inst
            pdb.set_trace()

    return d

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



