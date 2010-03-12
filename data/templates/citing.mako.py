from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1263584612.839
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/citing.mako'
_template_uri='/citing.mako'
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
        __M_writer(u'\n\n')
        # SOURCE LINE 4
        __M_writer(u'\n\n')
        # SOURCE LINE 23
        __M_writer(u'\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n<br/><br/>\n<br/>\n <a href="/copd/">Main</a> | <a href="/copd/links">Links</a> | Citing\n<br/>\n<br/><br/>\nHere is a link to the article on PubMed: <a href="http://www.ncbi.nlm.nih.gov/pubmed/19933216">http://www.ncbi.nlm.nih.gov/pubmed/19933216</a>\n<br/><br/>\nCastaldi PJ, Cho MH, Cohn M, Langerman F, Moran S, Tarragona N, Moukhachen H, Venugopal R, Hasimja D, Kao E, Wallace B, Hersh CP, Bagade S, Bertram L, Silverman EK, Trikalinos TA.\n<b>The COPD genetic association compendium: a comprehensive online database of COPD genetic associations.</b> Human Molecular Genetics. 2010 Feb 1;19(3):526-34. \n\n<br/>\n</br>\n\n\n\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head_tags(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


