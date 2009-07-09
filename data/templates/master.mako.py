from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1246043745.0320001
_template_filename=u'C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/master.mako'
_template_uri=u'/master.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html>\n  <title>COPDdb -- Tufts Medical Center</title>\n  <head>\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n    <script src="/javascripts/prototype.js" type="text/javascript"></script>\n    <script src="/javascripts/scriptaculous.js" type="text/javascript"></script>\n    <center>\n    <img src = "/images/header2.png">\n    </center>\n    ')
        # SOURCE LINE 13
        __M_writer(unicode(self.head_tags()))
        __M_writer(u'\n  </head>\n \n  <body>\n    <font face="Helvetica, sans-serif" style="font-family: Helvetica, sans-serif; font-size: 14px; color:black">\n    ')
        # SOURCE LINE 18
        __M_writer(unicode(self.body()))
        __M_writer(u'\n    </font>\n  <br/>\n  </body>\n  \n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


