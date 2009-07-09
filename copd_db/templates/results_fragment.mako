<center>
<%
    if c.img_path is None:
        context.write("Sorry, there was an error performing the meta-analysis.")
    else:
        context.write("<img src =" + c.img_path + "></img>")
%>


<h2>Data Used in Analysis</h2>

<table border="2" cellspacing="0" font-weight:"normal">
	  <tr>
	  <%
	  table_headers = ["study", "year", "num. cases", "num. controls"]
	  for header in table_headers:
	    context.write('<th>')
	    context.write(header)
	    context.write('</th>')
	  context.write('</tr>')
	  
	  
	  for study_index in range(len(c.data_used["study"])):
	    context.write('<tr>')
	    context.write('<td>' + str(c.data_used["study"][study_index]) + '</td>')
	    context.write('<td>' + str(c.data_used["year"][study_index]) + '</td>')
	    context.write('<td>' + str(float(c.data_used["n.e"][study_index]) / 2.0) + '</td>')
	    context.write('<td>' + str(float(c.data_used["n.c"][study_index]) / 2.0) + '</td>')
	    context.write('</tr>')      
	  %> 
</table>
</center>