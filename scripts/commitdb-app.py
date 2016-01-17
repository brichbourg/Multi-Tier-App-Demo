#!/usr/bin/python

import time
import cgi
import os.path


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

#process the data from the HTML form
form = cgi.FieldStorage()
arg1 = form.getvalue('name')
arg1 = arg1.replace("'","\\'") #keeps single quotes from crashing the app because of the SQL statement
arg2 = form.getvalue('notes')
arg2 = arg2.replace("'","\\'") #keeps single quotes from crashing the app because of the SQL statement
arg3 = form.getvalue('count')
arg3int = int(arg3) 
numofrecords = arg3int

#While loop to start entering the records into the MySQL server
while arg3int > 0:
	#this format the SQL state for the MySQL server
	forsql_name = "\'" + arg1 + "\'"
	forsql_notes = "\'" + arg2 + "\'"
	currentdatetime = time.strftime("%Y-%m-%d %H:%M:%S")
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