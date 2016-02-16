#!/usr/bin/python
from datetime import datetime
import cgi
import appsitefunctions
# Turn on debug mode.
import cgitb
cgitb.enable()

# Connect to the database.
import pymysql
try:
	conn = pymysql.connect(
	    db='appdemo',
	    user='appdemo',
	    passwd='appdemo',
	    host='dbserver-appdemo')
	c = conn.cursor()

	

	#process the data from the HTML form and check to see if data was entered.
	usercommand = 'nothing_entered'
	form = cgi.FieldStorage()

	if form.getvalue('command') == None:
		arg1 = 'null'
	else:
		arg1 = form.getvalue('command')
		usercommand = str.upper(arg1)

	#Used for the erase log
	currentdatetime = str(datetime.now())
	forsql_datetime = "\'" + currentdatetime + "\'"

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

	#Check the value of the string entered in the form and looks to see if the user entered the word "ERASE"
	if usercommand == 'ERASE':

		deletetable = "DROP TABLE  demodata"
		recreatetable = "CREATE TABLE `demodata` (`id` INTEGER NOT NULL AUTO_INCREMENT,`name` VARCHAR(100),`notes` TEXT,`timestamp` TIMESTAMP,PRIMARY KEY (`id`),KEY (`name`));"
		logdelete = "INSERT INTO demodata_erase_log VALUES(\'\',"+forsql_datetime+")"

		#Runs SQL command on MySQL database
		deleteresult = c.execute(deletetable)
		recreateresult = c.execute(recreatetable)
		c.execute(logdelete)

		# Checks to see if the anything other than 1 is returned from c.execute() function calls
		if deleteresult == 0:
			if recreateresult == 0:
				print '<br><center><h3>Data Erased From Database!</center></h3>'
		else:
			print '<br><center><h3>There was an error deleting the information to the database</h3></center>'

		conn.commit()
	else:
		print '<br><center><font color="red">Data NOT Cleared.  No command or incorrect command was entered.</font></center>'

	print '</center>'

	#Finish printing headers 
	print '''
	</table>
	</body>
	</html>
	'''

except:
	appsitefunctions.printdbservererror()
