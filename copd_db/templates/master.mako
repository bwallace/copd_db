# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <title>COPDdb -- Tufts Medical Center</title>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    ${ h.stylesheet_link_tag( '/master.css') } 
    <script src="/javascripts/prototype.js" type="text/javascript"></script>
    <script src="/javascripts/scriptaculous.js" type="text/javascript"></script>
    <script>

    //Sortable table script- Han Yu han@velocityhsi.com
    //Script featured on http://www.javascriptkit.com
    var domok=document.all||document.getElementById
    if (domok)
    document.write('<SCRIPT SRC="/scripts/sortTable.js"><\/SCRIPT>')
    </script>
    
    <center>
    <img src = "/images/header2.png">
    </center>
    ${self.head_tags()}
  </head>
 
  <body>
    <div id='wrapper'>
        ${self.body()}
    </div>
    

  </body>
  
</html>