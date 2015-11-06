#!/usr/bin/python

#This is a "modlue" script, which I mean that appsitefunctions.loadbasehtml() uses this to create a section of the site.

print '<!-- Start of form -->'
print '<center>'
print '<table>'
print '<tr>'
print '<td>'
print '<form action="cleardb.py" method="POST" id="usrform">'
print '  <b><br> Enter <font color="red">ERASE </font>to clear the database:</b><br>'
print '  <input type="text" name="command" value="">'
print '  <br><br>'
print '  <input type="submit" value="Submit">'
print '</form>'
print '</td>'
print '</tr>'
print '</table>'

print '</center>'
