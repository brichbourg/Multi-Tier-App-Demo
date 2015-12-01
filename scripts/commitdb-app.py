#!/usr/bin/python

from datetime import datetime
import cgi
import os.path
import appsitefunctions

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

#This will call the fucntion to loab the base.html file for the site.
modulename = None #This needs to be used when we are not using the index.py script.  This is for loading the 'custom mode' which is not needed here.
# appsitefunctions.printsite(modulename)

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
	sqlstring = "INSERT INTO demodata VALUES(0,"+forsql_name+","+forsql_notes+","+forsql_datetime+")"
	
	#Saves data to MySQL database
	result = c.execute(sqlstring)
	conn.commit()
	arg3int -=1

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

# Checks to see if the anything other than 1 is returned from c.execute()
if result == 1:
	if numofrecords == 1:
		print '<br><center><h3>Saved %s Record to Database!</h3></center>' %numofrecords
	else:
		print '<br><center><h3>Saved %s Records to Database!</h3></center>' %numofrecords
else:
	print '<h3>There was an error commiting the information to the database</h3>'

print '</center>'

#Finish printing headers 
print '''
</table>
</body>
</html>
'''