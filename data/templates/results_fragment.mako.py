from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1248209392.0
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/results_fragment.mako'
_template_uri='/results_fragment.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<center>\n    \n<br/>\n<h2>forest plot</h2>\n')
        # SOURCE LINE 5

        if c.img_path is None:
            context.write("Sorry, there was an error performing the meta-analysis.")
        else:
            context.write("<img src =" + c.img_path + "></img>")
        
        
        # SOURCE LINE 10
        __M_writer(u'\n\n\n<h2>analysis details</h2>\n\nShow:\n<select id="DisplayedResults" name="DisplayedResults" style="width:200px" onchange="\nnew Ajax.Updater(\n    \'table_results\',\n    \'/copd/update_displayed_data/\',\n    {\n        onComplete:function(){ new Effect.Highlight(\'table_results\', duration=4);},\n        asynchronous:true,\n        evalScripts:true,\n        parameters:{\'DisplayThis\': $(\'DisplayedResults\').value}\n    }\n);\n">\n\n<option value="table" selected="selected" size = 300>')
        # SOURCE LINE 29
        __M_writer(unicode( "Data table"))
        __M_writer(u'</option>\n<option value="demographics"  size = 300>')
        # SOURCE LINE 30
        __M_writer(unicode( "Demographics"))
        __M_writer(u'</option>\n\n\n</select>\n<br/><br/>\n\n<div id = "table_results">\n\n<table class="pretty">\n\t  ')
        # SOURCE LINE 39
        __M_writer(unicode(c.table))
        __M_writer(u'\n</table>\n</div>\n</center>')
        return ''
    finally:
        context.caller_stack._pop_frame()


