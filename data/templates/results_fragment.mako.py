from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1245286678.1500001
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/results_fragment.mako'
_template_uri='/results_fragment.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        len = context.get('len', UNDEFINED)
        range = context.get('range', UNDEFINED)
        float = context.get('float', UNDEFINED)
        c = context.get('c', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'<center>\n')
        # SOURCE LINE 2

        if c.img_path is None:
            context.write("Sorry, there was an error performing the meta-analysis.")
        else:
            context.write("<img src =" + c.img_path + "></img>")
        
        
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin()[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin()]))
        # SOURCE LINE 7
        __M_writer(u'\n\n\n<h2>Data Used in Analysis</h2>\n\n<table border="2" cellspacing="0" font-weight:"normal">\n\t  <tr>\n\t  ')
        # SOURCE LINE 14

        table_headers = ["study", "year", "num. cases", "num. controls"]
        for header in table_headers:
          context.write('<th>')
          context.write(header)
          context.write('</th>')
        context.write('</tr>')
        
        
        for study_index in range(len(c.data_used["study"])):
          context.write('<tr>')
          context.write('<td>' + str(c.data_used["study"][study_index]) + '</td>')
          context.write('<td>' + str(c.data_used["year"][study_index]) + '</td>')
          context.write('<td>' + str(float(c.data_used["n.e"][study_index]) / 2.0) + '</td>')
          context.write('<td>' + str(float(c.data_used["n.c"][study_index]) / 2.0) + '</td>')
          context.write('</tr>')      
        
        
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin()[__M_key]) for __M_key in ['header','table_headers','study_index'] if __M_key in __M_locals_builtin()]))
        # SOURCE LINE 30
        __M_writer(u' \n</table>\n</center>')
        return ''
    finally:
        context.caller_stack._pop_frame()


