#!/usr/bin/python

# Turn on debug mode.
import cgitb
cgitb.enable()

# Print necessary headers.
print 'Content-type: text/html\n\n'

# Connect to the database.
import pymysql
conn = pymysql.connect(
    db='appdemo',
    user='appdemo',
    passwd='appdemo',
    host='dbserver-appdemo')
c = conn.cursor()

# State of main HTML output
print '<html>'
print '<head>'
print '<title>Brantley\'s Python Web Script </title>'
print '</head>'
print '\n'
print '<body>'

#Here is just some pretty stuff
print '<center>'
print '<IMG SRC="logo.jpg"></IMG>'
print '<h1> Multi-Tier Application Example </h1>'
print '<h3> View Data </h3>'
print '</center>'

#menu
print '<center>'
print '<table border="10" bgcolor="#71bf45">'

print '<tr>'
print '<td><br><center><form action="index.html"><input type="submit" value="Main Menu"></center></form></td>'
print '</tr>'
print '</table>'
print '</center>'

#Now lets make a table with the database contents
print '\n <br> <br>'
print '<center>'
print 'Database Contents'
print '<table style="width:100%" border="1">'

# # Print the contents of the database.
c.execute("SELECT * FROM demodata")

#Start printing the html for the header row
print '<tr>'
print '<td><b>ID</b></td>'
print '<td><b>Name</b></td>'
print '<td><b>Notes</b></td>'
print '<td><b>Timestamp</b></td>'
print '</tr>'

#now to print within the table with the contents of the database
for each in c.fetchall():
	print '<tr>'
 	print '<td>',each[0], '</td>'
 	print '<td>',each[1], '</td>'
 	print '<td>',each[2], '</td>'
 	print '<td>',each[3], '</td>'
 	print '</tr>'

print '</table>'
print '</center>'

print '</body>'
print '\n'
print '</html>'

