#!/usr/bin/python


#This is a "module" script, by which I mean that appsitefunctions.loadbasehtml() uses this to create a section of the site.

# Turn on debug mode.
import cgitb
cgitb.enable()

# Connect to the database.
import pymysql
conn = pymysql.connect(
    db='appdemo',
    user='appdemo',
    passwd='appdemo',
    host='dbserver-appdemo')
c = conn.cursor()
			
#Grab the table data from the database.
c.execute("SELECT * FROM demodata")

#Start HTML print out, headers are printed so the Apache server on APP does not produce a malformed header 500 server error
print '''
<Content-type: text/html\\n\\n>
<html>
<head>
<title>Multi-Tier Web App</title>
</head>
<body>
<table border="1">
'''

#Start printing the html for the header row
print '<center><h3>View Data</h3></center>'
print '<table style="width:100%" border="1">'
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

#Finish printing headers 
print '''
</table>
</body>
</html>
'''

