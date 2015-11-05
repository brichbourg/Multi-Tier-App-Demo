#!/usr/bin/python
from datetime import datetime
import cgi

# Turn on debug mode.
import cgitb
cgitb.enable()

# # Print necessary headers.
# print 'Content-type: text/html\n\n'

# Connect to the database.
import pymysql
conn = pymysql.connect(
    db='appdemo',
    user='appdemo',
    passwd='appdemo',
    host='dbserver-appdemo')
c = conn.cursor()

#This will import the index.py script to print the main menu, etc.  Did this so I did not have to rewrite for this script.
import index

#process the data from the HTML form and check to see if data was entered.
usercommand = 'nothing_entered'
form = cgi.FieldStorage()

print form, ':(DEBUG): VALUE RECEIVED FROM THE FORM ' #db

if form.getvalue('command') == None:
	arg1 = 'null'
else:
	arg1 = form.getvalue('command')
	usercommand = str.upper(arg1)

#Used for the erase log
currentdatetime = str(datetime.now())
forsql_datetime = "\'" + currentdatetime + "\'"

#Check the value of the string entered in the form and looks to see if the user entered the word "ERASE"
if usercommand == 'ERASE':

	deletetable = "DROP TABLE  demodata"
	# print deletetable, ' :--deletetabel<br><br>' #debug
	recreatetable = "CREATE TABLE `demodata` (`id` INTEGER NOT NULL AUTO_INCREMENT,`name` VARCHAR(100),`notes` TEXT,`timestamp` TIMESTAMP,PRIMARY KEY (`id`),KEY (`name`));"
	logdelete = "INSERT INTO demodata_erase_log VALUES(\'\',"+forsql_datetime+")"

	#Runs SQL command on MySQL database
	deleteresult = c.execute(deletetable)
	recreateresult = c.execute(recreatetable)
	c.execute(logdelete)

	# Checks to see if the anything other than 1 is returned from c.execute() function calls
	if deleteresult == 0:
		if recreateresult == 0:
			print '<br><h3>Data Erased From Database!</h3>'
	else:
		print '<br><h3>There was an error deleting the information to the database</h3>'

	conn.commit()
else:
	# print 'else statement' #debug
	print '<br><center><font color="red">Data NOT Cleared.  Incorrect command entered.</font></center>'

print '</center>'

# print '</body>'
# print '\n'
# print '</html>'

