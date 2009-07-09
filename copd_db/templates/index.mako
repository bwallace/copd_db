
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
        parameters:{'GeneName': $('GeneName').value}
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
</center>

<div id="results" style='float: center'>
<br/>


<b>Welcome to COPDdb &beta;</b>. 
<br/><br/>

Some notes on our data. First, this database is up-to-date as of July 2008. Second, the unit of analysis for each meta-analysis is a comparison between a group of COPD cases, and a corresponding control group of comparable racial descent. For studies comparing several (more than one) groups of cases versus a common control group, we divided the counts in the controls into subgroups of equal size, and entered the study as several independent meta-analysis entries. This avoids double or triple counting the controls.  The corresponding thing was done when one group of cases was compared with several control groups. 
<br/><br/>
To run an analysis, first select a gene and then select a polymorphism from the two combo boxes, above. A meta-analysis will be conducted over this gene/polymorphism pair, and the results will be displayed on this webpage. 

</div>



</%def>