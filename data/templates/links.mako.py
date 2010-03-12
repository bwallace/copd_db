from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1263582769.4560001
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/links.mako'
_template_uri='/links.mako'
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
        # SOURCE LINE 52
        __M_writer(u'\n</html>')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n\n<br/>\n <a href="/copd/">Main</a> | Links | <a href="/copd/citing">Citing</a>\n<br/>\n\n\n<br/>\n<br/>\n<center>\n<table class="pretty">\n<tr>\n<th>HuGE</th>\n</tr>\n<tr>\n<td><a href="http://www.cdc.gov/genomics/hugenet/default.htm">HuGENet </a></td>\n</tr>\n<tr>\n<td><a href="http://hugenavigator.net">HuGE Navigator</a></td>\n</tr>\n</tr>\n</table>\n\n\n<table class="pretty">\n<tr>\n<th>Online Genetic Association Compendia</th>\n</tr>\n<tr>\n\n<td><a href="http://www.pdgene.org/">Parkinson\'s Disease </a></td>\n</tr>\n<tr>\n<td><a href="http://www.alzgene.org/">Alzheimer\'s Disease </a></td>\n</tr>\n<tr>\n<td><a href="http://www.schizophreniaforum.org/res/sczgene/default.asp">Schizophrenia</a></td>\n</tr>\n</tr>\n</table>\n</center>\n<br/>\n\n\n\n\n')
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


