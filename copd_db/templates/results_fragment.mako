<center>
    
<br/>
<h2>forest plot</h2>
<%
    if c.img_path is None:
        context.write("Sorry, there was an error performing the meta-analysis.")
    else:
        context.write("<img src =" + c.img_path + "></img>")
%>


<h2>analysis details</h2>

Show:
<select id="DisplayedResults" name="DisplayedResults" style="width:200px" onchange="
new Ajax.Updater(
    'table_results',
    '/copd/update_displayed_data/',
    {
        onComplete:function(){ new Effect.Highlight('table_results', duration=4);},
        asynchronous:true,
        evalScripts:true,
        parameters:{'DisplayThis': $('DisplayedResults').value}
    }
);
">

<option value="demographics" selected="selected" size = 300>${ "Demographics"}</option>
<option value="table" selected="selected" size = 300>${ "Data table"}</option>

</select>
<br/><br/>

<div id = "table_results">
<table class = "pretty">
	  ${c.table}
</table>
</div>
</center>