#!/usr/bin/python
import os.path
import cgi
import socket
import os
import urllib
import time

# Turn on debug mode.
import cgitb
cgitb.enable()

#loads data from the mtwa.conf file to be used in the application
def importconfiguration (): 
	if os.path.exists('/etc/mtwa/mtwa.conf'):
		mtwaconf = open('/etc/mtwa/mtwa.conf').read().splitlines()

		for each in mtwaconf: 

			if each == '#': #This skips lines that start with #, as they are comments
				continue 
			else:

				if each[:13] == "AppServerName":
					AppServerName = each[13:]

					for char in AppServerName: #will remove the = and whitespace characters to return the DNS or IP addresses configred in mtwa.conf
						AppServerName = AppServerName.lstrip()
						AppServerName = AppServerName.lstrip("=")
						AppServerName = AppServerName.rstrip()

				if each[:12] == "DBServerName":
					DBServerName = each[12:]

					for char in DBServerName: #will remove the = and whitespace characters to return the DNS or IP addresses configred in mtwa.conf
						DBServerName = DBServerName.lstrip()
						DBServerName = DBServerName.lstrip("=")
						DBServerName = DBServerName.rstrip()

		return (AppServerName,DBServerName)


	else:
		print 'ERROR: MTWA Configuration file ', os.path.realpath('/etc/mtwa/mtwa.conf'), 'is missing!'

def printappservererror():

	print "<FONT COLOR='red'><H2>ERROR: APPLICATION SERVER UNAVAILABLE</H2></FONT>"

def printdbservererror():

	#Start HTML print out, headers are printed so the Apache server on APP does not produce a malformed header 500 server error
	print '''
	<Content-type: text/html\\n\\n>
	<html>
	<head>
	<title></title>
	</head>
	<body>
	<table border="1">
	'''

	print "<FONT COLOR='red'><H2>ERROR: DATABASE SERVER UNAVAILABLE</H2></FONT>"

	#Finish printing headers 
	print '''
	</table>
	</body>
	</html>
	'''

def getserverparam(param_name):

	# print param_name, "param_name<BR>" #db
    
	for each in os.environ.keys():	
		#Uncomment the next line if you want to see all of the values that could be used
		#print (each, os.environ[each]), "<br>" #db
		#print each, ":each <br>" #db

		each_value = os.environ[each]

		each_value_string = str(each_value)

		each_string = str(each)

		if each_string == param_name:			
			servervalue = each_value_string
			return servervalue


	return None
	
def setcolor(protocolvalue):
	if protocolvalue == 'HTTP':
		return 'red'
	elif protocolvalue == 'HTTPS':
		return 'green'
	else:
		return 'black'

def finddnsresolver():
	#This function will find the local DNS server to be used in another function for finding the IP address of the host.
	dnsfile = open('/etc/resolv.conf').read().splitlines()
	for each in dnsfile:
		nameserverstring = each[:10]
		if nameserverstring == "nameserver":
			dns_ip = each[11:]
			return dns_ip
	return None

def removehtmlheaders(htmlcode):
	#This function is designed to remove the HTML headers that are adder so that Apache on the APP server will not give a 500 error due to bad headers.
	splitcode = htmlcode.split('\n')

	#Delete the first 7 elements in the list.  This is the first section of generic HTML code to be removed.
	deletecount = 7
	while deletecount > 0:
		del splitcode[0]
		deletecount-=1
	
	#Delete the last 5 elements in the list.  This is the last section of generic HTML code to be removed.
	listposition = int(len(splitcode) - 1)
	deletecount = 5
	while deletecount > 0:
		del splitcode[listposition]
		listposition -=1
		deletecount-=1

	noheaderhtml = '\n'.join(splitcode)
	return noheaderhtml

def getserverinfo():
	#This code establishes a connection to the DNS server to get the host's IP address.  This is to get the real IP address.  
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.connect((finddnsresolver(),53)) # sock.connect(("nameserver",53))
	ipaddress=(sock.getsockname()[0])
	sock.close()

	#This get the hostname as defined in /etc/hostname
	hostname = (socket.gethostname())

	#Use OS environment variables gather information
	serverport = getserverparam('SERVER_PORT')
	
	if getserverparam('REQUEST_SCHEME') != None:  
		serverprotocol = str.upper(getserverparam('REQUEST_SCHEME'))
	
		return (hostname,ipaddress,serverprotocol,serverport)
	else:
		serverprotocol = 'Unknown'
		return (hostname,ipaddress,serverprotocol,serverport)

	#IF YOU WANT TO FIGURE OUT WHAT VARIABLES CAN BE USED, UNCOMMENT THE NEXT LINE TO ADD OTHER INFORMATION AND REFRESH THE WEBPAGE
	# cgi.test() 

def getclientinfo():
	#Gathers client information
	clientip = getserverparam('REMOTE_ADDR')
	# print 'clientip', clientip #db
	clientport = getserverparam('REMOTE_PORT')
	# print 'clientport', clientport #db
	x4ed4 = getserverparam('HTTP_X_FORWARDED_FOR')
	# print 'x4ed4', x4ed4 #db
	return (clientip,clientport,x4ed4)

def enterdbformhtml():
	
	print '<center>'
	print '<table>'
	print '<tr>'
	print '<td>'
	print '<form action="commitdb-web.py" method="POST" id="usrform">'
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

def cleardbformhtml():

	print '<!-- Start of form -->'
	print '<center>'
	print '<table>'
	print '<tr>'
	print '<td>'
	print '<form action="cleardb-web.py" method="POST" id="usrform">'
	print '  <b><br> Enter <font color="red">ERASE </font>to clear the database:</b><br>'
	print '  <input type="text" name="command" value="">'
	print '  <br><br>'
	print '  <input type="submit" value="Submit">'
	print '</form>'
	print '</td>'
	print '</tr>'
	print '</table>'

	print '</center>'

def printserverinfo(hostname,ipaddress,webprotocol,serverport):

	localtime = time.strftime("%Y-%m-%d %H:%M:%S")


	protocol_color = setcolor(webprotocol)
	print '<tr><td align="right">Hostname:</td><td>%s<br></td></tr>'%hostname
	print '<tr><td align="right">IPv4:</td><td>%s<br></td></tr>' %ipaddress
	print '<tr><td align="right">Protocol: </td><td><B><font color=\"%s\">%s</B><br></td></tr>'% (protocol_color, webprotocol)
	print '<tr><td align="right">Port: </td><td>%s<br></td></tr>'%serverport
	print '<tr><td align="right">Application Version:</td><td>0.6.1<br></td></tr></font>'
	print '<tr><td align="right">Local System Time:</td><td>%s<br></td></tr>' %localtime

	
def printsite(modulename,formname_or_cmd,formnotes,formcount):

	if os.path.exists('base.html'):
		basehtml = open('base.html').read().splitlines()

		print 'Content-type: text/html\n\n'

		#This gets and sets the values for the server
		clientvalues = getclientinfo()
		clientipaddress = clientvalues[0]
		clientportnum = clientvalues[1]
		forwarded_for = clientvalues[2]
		servervalues = getserverinfo()
		host = servervalues[0]
		ipaddress = servervalues[1]
		webprotocol = servervalues[2]
		port = servervalues[3]

		#This section will grab the name of the app server host name from the mtwa.conf file
		servernames=importconfiguration() 
		AppServerHostname=servernames[0]

		for each in basehtml: 
			print each #This will print the lines from base.html that is loaded into the FOR LOOP
			
			#This prints the server information in the HTML title.
			if each == '<!-- StartTitleInfo -->':

				# print 'StartTitleInfo' #db
				print '<title>%s / %s [%s]</title>'%(host,ipaddress,webprotocol)

			if each == '<!-- StartClientInfo -->':

				#This will print the table row information for the client information table
				print '<tr><td align="right">IPv4:</td><td>%s<br></td></tr>' %clientipaddress
				print '<tr><td align="right">Port:</td><td>%s<br></td></tr>' %clientportnum
				print '<tr><td align="right">X_Forwarded_For:</td><td>%s<br></td></tr>' %forwarded_for

			#This print the local web server information
			if each == '<!-- StartWebServerInfo -->':
				
				#This will print that infomation for the HTML table in base.html
				printserverinfo(host,ipaddress,webprotocol,port)

			#This print the local web server information
			if each == '<!-- StartAppServerInfo -->':

				#This gets and sets the values for the app server 
				try:
					appserverresponse = urllib.urlopen('http://%s:8080/appserverinfo.py'%AppServerHostname)
					appserverhtml = removehtmlheaders(appserverresponse.read())
					print appserverhtml
				except:
					print '<table border="0"><tr><td>Hostname:</td><td><font color="red">ERROR</font><br></td></tr><tr><td>IPv4:</td><td><font color="red">ERROR</font><br></td></tr><tr><td>Protocol: </td><td><font color="red">ERROR</font><br></td></tr><tr><td>Port: </td><td><font color="red">ERROR</font><br></td></tr><tr><td>Application Version:</td><td><font color="red">ERROR</font><br></td></tr></font><tr><td>Local System Time:</td><td><font color="red">ERROR</font><br></td></tr></table>'

			if each == '<!-- StartCustom -->':
				#This uses to value passed from the URL to basically set which .py script is used for this section.
				if modulename != None:
					if modulename == 'enterdb':
						enterdbformhtml()
					elif modulename == 'resetdb':
						cleardbformhtml()
					elif modulename == 'commitdb':
						#Here formname_or_cmd is used as the NAME which was entered into the form
						try:
							urlstr = 'http://%s:8080/commitdb-app.py?name=%s&notes=%s&count=%s'%(AppServerHostname,formname_or_cmd,formnotes,formcount)
							appserverresponse = urllib.urlopen(urlstr)
							appserverhtml = removehtmlheaders(appserverresponse.read())
							print appserverhtml
						except:
							printappservererror()

					elif modulename == 'cleardb':
						#Here formname_or_cmd is used as the COMMAND which was entered into the form
						try:
							urlstr = 'http://%s:8080/cleardb-app.py?command=%s'%(AppServerHostname,formname_or_cmd)
							appserverresponse = urllib.urlopen(urlstr)
							appserverhtml = removehtmlheaders(appserverresponse.read())
							print appserverhtml
						except:
							printappservererror()
					else:
						try:
							urlstr = 'http://%s:8080/%s.py'%(AppServerHostname,modulename)
							appserverresponse = urllib.urlopen(urlstr)
							appserverhtml = removehtmlheaders(appserverresponse.read())
							print appserverhtml
						except:
							printappservererror()
			
		

		

			
	else:
		print 'ERROR: Base HTML file ', os.path.realpath('base.html'), 'is missing'



				