from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 4
_modified_time = 1253124100.5910001
_template_filename='C:\\dev\\copd\\copddb\\copd_db\\copd_db\\templates/polymorphism_fragment.mako'
_template_uri='/polymorphism_fragment.mako'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding=None
_exports = []


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        set = context.get('set', UNDEFINED)
        list = context.get('list', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n<select id="Polymorphism" name="Polymorphism" style="width:200px" onchange="\nnew Ajax.Updater(\n    \'results\',\n    \'/copd/polymorphism_selected/\',\n    {\n        onCreate:function(){new Effect.Appear(\'busy\', duration=4)},\n        \n        onComplete:function(){ new Effect.Highlight(\'results\', duration=4);},\n        onComplete:function(){new Effect.Fade(\'busy\')},\n        asynchronous:true,\n        evalScripts:true,\n        parameters:{\'Polymorphism\': $(\'Polymorphism\').value, \'Gene\':')
        # SOURCE LINE 14
        __M_writer(unicode("'" + c.gene_name + "'"))
        __M_writer(u' }\n    }\n);\n">\n<option value="" selected="selected" size = 50>Select a polymorphism...</option>\n  ')
        # SOURCE LINE 19

        polymorphisms = list(set([association.polymorphism for association in c.associations]))
        polymorphisms.sort()
        for polymorphism in polymorphisms:
            if not polymorphism == "":
                context.write("<option value = '%s'>%s</option>" % (polymorphism, polymorphism))
          
        
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin()[__M_key]) for __M_key in ['polymorphisms','association','polymorphism'] if __M_key in __M_locals_builtin()]))
        # SOURCE LINE 25
        __M_writer(u' \n</select>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


