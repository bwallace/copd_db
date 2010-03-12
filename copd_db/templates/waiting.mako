<center>
    
<br/>

<%
    if c.img_path is None:
        context.write("Sorry, there was an error performing the meta-analysis.")
    else:
        context.write("<img src = '/images/loading.gif'></img>")
%>



</div>
</center>