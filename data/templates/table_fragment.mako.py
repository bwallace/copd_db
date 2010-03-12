from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1247175004.348
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/table_fragment.mako'
_template_uri='/table_fragment.mako'
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
        __M_writer(u'<table class = "pretty">\n    ')
        # SOURCE LINE 2
        __M_writer(unicode(c.table))
        __M_writer(u'\n</table>')
        return ''
    finally:
        context.caller_stack._pop_frame()


