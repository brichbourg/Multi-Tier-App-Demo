#!/usr/bin/python

print '<center>'
print '<table>'
print '<tr>'
print '<td>'
print '<form action="commitdb.py" method="POST" id="usrform">'
print '  <b>Name:</b><br>'
print '  <input type="text" name="name" value="Mickey Mouse">'
print '  <br><br>'
print '  <b>Notes:</b><br>'
print '  <textarea rows="6" cols="50" name="notes" form="usrform">Hot Dog, Hot Dog, Hot Diggy Dog!</textarea>'
print '  <br><br>'
print '  <b>Number of records to create:</b><br>'
print '  <input type="number" name="count" min="1" max="1000" value="1">'
print '  <br><br>'
print '  <input type="submit" value="Submit">'
print '</form>'
print '</td>'
print '</tr>'
print '</table>'
print '</center>'


