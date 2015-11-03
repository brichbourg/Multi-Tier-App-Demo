#!/usr/bin/python
from datetime import datetime
import cgi
# Turn on debug mode.
import cgitb
cgitb.enable()

# Print necessary headers.
print 'Content-type: text/html\n\n'

# Connect to the database.
import pymysql
conn = pymysql.connect(
    db='appdemo',
    user='root',
    passwd='Labserver1',
    host='localhost')
c = conn.cursor()


# Brantley's Code
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
print '<h3> Commit Data </h3>'
print '</center>'


print '\n'
print '<center>'

#menu
print '<center>'
print '<table border="10" bgcolor="#71bf45">'

print '<tr>'
print '<td><br><center><form action="index.html"><input type="submit" value="Main Menu"></center></form></td>'
print '</tr>'
print '</table>'
print '</center>'

#process the data from the HTML form
form = cgi.FieldStorage()
arg1 = form.getvalue('name')
arg2 = form.getvalue('notes')
arg3 = form.getvalue('count')
arg3int = int(arg3) 
numofrecords = arg3int

#While loop to start entering the records into the MySQL server
while arg3int > 0:
	#this format the SQL state for the MySQL server
	forsql_name = "\'" + arg1 + "\'"
	forsql_notes = "\'" + arg2 + "\'"
	currentdatetime = str(datetime.now())
	forsql_datetime = "\'" + currentdatetime + "\'"
	sqlstring = "INSERT INTO demodata VALUES(\'\',"+forsql_name+","+forsql_notes+","+forsql_datetime+")"
	
	#Saves data to MySQL database
	result = c.execute(sqlstring)
	conn.commit()
	arg3int -=1

# Checks to see if the anything other than 1 is returned from c.execute()
if result == 1:
	if numofrecords == 1:
		print '<br><h3>Saved %s Record to Database!</h3>' %numofrecords
	else:
		print '<br><h3>Saved %s Records to Database!</h3>' %numofrecords
else:
	print '<h3>There was an error commiting the information to the database</h3>'



print '</center>'

print '</body>'
print '\n'
print '</html>'

