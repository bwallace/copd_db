from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1253109707.7019999
_template_filename=u'C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/master.mako'
_template_uri=u'/master.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n  <title>COPDdb -- Tufts Medical Center</title>\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n    ')
        # SOURCE LINE 8
        __M_writer(unicode( h.stylesheet_link_tag( '/master.css') ))
        __M_writer(u' \n    <script src="/javascripts/prototype.js" type="text/javascript"></script>\n    <script src="/javascripts/scriptaculous.js" type="text/javascript"></script>\n    <script>\n\n    //Sortable table script- Han Yu han@velocityhsi.com\n    //Script featured on http://www.javascriptkit.com\n    var domok=document.all||document.getElementById\n    if (domok)\n    document.write(\'<SCRIPT SRC="/scripts/sortTable.js"><\\/SCRIPT>\')\n    </script>\n    \n    <center>\n    <img src = "/images/header2.png">\n    </center>\n    ')
        # SOURCE LINE 23
        __M_writer(unicode(self.head_tags()))
        __M_writer(u"\n  </head>\n \n  <body>\n    <div id='wrapper'>\n        ")
        # SOURCE LINE 28
        __M_writer(unicode(self.body()))
        __M_writer(u'\n    </div>\n    \n\n  </body>\n  \n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


