from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1253123731.635
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/index.mako'
_template_uri='/index.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = ['body', 'head_tags']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'master.mako', _template_uri)
def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u"\n# -*- coding: utf-8 -*-\n#onComplete:function(){ new Effect.Highlight('results', duration=4);},\n")
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 7
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body(context):
    context.caller_stack._push_frame()
    try:
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 9
        __M_writer(u'\n\n<center>\n\n<br/>\n<select id="GeneName" name="GeneName" style="width:200px" onchange="\nnew Ajax.Updater(\n    \'polymorphism_select\',\n    \'/copd/gene_selected/\',\n    {\n        onComplete:function(){ new Effect.Highlight(\'polymorphism_select\', duration=4);},\n        asynchronous:true,\n        evalScripts:true,\n        parameters:{\'GeneName\': $(\'GeneName\').value}\n    }\n);\n">\n<option value="" selected="selected">')
        # SOURCE LINE 26
        __M_writer(unicode(c.currently_selected_gene.gene_name if c.currently_selected_gene else "Select a gene..."))
        __M_writer(u'</option>\n  ')
        # SOURCE LINE 27

        genes = [gene.gene_name for gene in c.all_genes]
        genes.sort()
        for gene  in genes:
            if not gene == "":
                context.write("<option value = '%s'>%s</option>" % (gene, gene))
          
        
        # SOURCE LINE 33
        __M_writer(u' \n</select>\n\n<br/><br/>\n\n<div id = "polymorphism_select">\n<select id="Polymorphism" name="Polymorphism" style="width:200px" onchange="\nnew Ajax.Updater(\n    \'results\',\n    \'/copd/polymorphism_selected/\',\n    {\n        \n        onCreate:function(){ new Effect.Highlight(\'results\', duration=4);},\n        asynchronous:true,\n        evalScripts:true,\n        parameters:{\'Polymorphism\': $(\'Polymorphism\').value}\n    }\n);\n">\n<option value="" selected="selected" size = 300>')
        # SOURCE LINE 52
        __M_writer(unicode( "No gene selected yet."))
        __M_writer(u'</option>\n</select>\n</div>\n</center>\n\n\n<div id="busy" style = \'display:none\'><center><img src = "images/loading.gif"></img></center></div>\n\n\n<div id="results" style=\'float: center\'>\n<br/>\n\n\n<b>Welcome to COPDdb &beta;</b>. \n<br/><br/>\n\nSome notes on our data. First, this database is up-to-date as of July 2008. Second, the unit of analysis for each meta-analysis is a comparison between a group of COPD cases, and a corresponding control group of comparable racial descent. For studies comparing several (more than one) groups of cases versus a common control group, we divided the counts in the controls into subgroups of equal size, and entered the study as several independent meta-analysis entries. This avoids double or triple counting the controls.  The corresponding thing was done when one group of cases was compared with several control groups. \n<br/><br/>\nTo run an analysis, first select a gene and then select a polymorphism from the two combo boxes, above. A meta-analysis will be conducted over this gene/polymorphism pair, and the results will be displayed on this webpage. \n\n</div>\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


