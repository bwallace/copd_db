

<select id="Polymorphism" name="Polymorphism" style="width:200px" onchange="
new Ajax.Updater(
    'results',
    '/copd/polymorphism_selected/',
    {
        onCreate:function(){new Effect.Appear('busy', duration=4)},
        
        onComplete:function(){ new Effect.Highlight('results', duration=4);},
        onComplete:function(){new Effect.Fade('busy')},
        asynchronous:true,
        evalScripts:true,
        parameters:{'Polymorphism': $('Polymorphism').value, 'Gene':${"'" + c.gene_name + "'"} }
    }
);
">
<option value="" selected="selected" size = 50>Select a polymorphism...</option>
  <%
            polymorphisms = list(set([association.polymorphism for association in c.associations]))
            polymorphisms.sort()
            for polymorphism in polymorphisms:
                if not polymorphism == "":
                    context.write("<option value = '%s'>%s</option>" % (polymorphism, polymorphism))
  %> 
</select>

