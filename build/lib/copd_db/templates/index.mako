
# -*- coding: utf-8 -*-
<%inherit file="master.mako" />

<%def name="head_tags()">
</%def>

<%def name="body()">

<center>

<br/>
<select id="GeneName" name="GeneName" style="width:200px" onchange="
new Ajax.Updater(
    'polymorphism_select',
    '/copd/gene_selected/',
    {
        onComplete:function(){ new Effect.Highlight('polymorphism_select', duration=4);},
        asynchronous:true,
        evalScripts:true,
        parameters:{'GeneName': $('GeneName').value},
    }
);
">
<option value="" selected="selected">${c.currently_selected_gene.gene_name if c.currently_selected_gene else "Select a gene..."}</option>
  <%
    genes = [gene.gene_name for gene in c.all_genes]
    genes.sort()
    for gene  in genes:
        if not gene == "":
            context.write("<option value = '%s'>%s</option>" % (gene, gene))
  %> 
</select>

<br/><br/>

<div id = "polymorphism_select">
<select id="Polymorphism" name="Polymorphism" style="width:200px" onchange="
new Ajax.Updater(
    'results',
    '/copd/polymorphism_selected/',
    {
        onComplete:function(){ new Effect.Highlight('results', duration=4);},
        asynchronous:true,
        evalScripts:true,
        parameters:{'Polymorphism': $('Polymorphism').value}
    }
);
">
<option value="" selected="selected" size = 300>${ "No gene selected yet."}</option>
</select>
</div>

<div id="results" style='float: center'>
<br/>
Nothing yet.
</div>
</center>


</%def>