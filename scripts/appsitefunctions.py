#!/usr/bin/python
import os.path
import cgi
import socket
import os
import urllib

# Turn on debug mode.
import cgitb
#cgitb.enable()

def getserverparam(param_name):

	# print param_name, "param_name<BR>" #db

	for each in os.environ.keys():	
		#Uncomment the next line if you want to see all of the values that could be used
		# print (each, os.environ[each]), "<br>" #db
		# print each, ":each <br>" #db

		each_value = os.environ[each]
		# print each_value, ":each_value <BR>" #db

		each_value_string = str(each_value)
		# print each_value_string, "each_value_string<BR>" #db

		each_string = str(each)
		# print each_value_string, ":each_value_string <BR>" #db

		if each_string == param_name:			
			servervalue = each_value_string
			# print servervalue, "servervalue<BR>" #db
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

def printserverinfo(hostname,ipaddress,webprotocol,serverport, printblank):

	if printblank == False:
		protocol_color = setcolor(webprotocol)
		print '<tr><td align="right">Hostname:</td><td>%s<br></td></tr>'%hostname
		print '<tr><td align="right">IPv4:</td><td>%s<br></td></tr>' %ipaddress
		print '<tr><td align="right">Protocol: </td><td><B><font color=\"%s\">%s</B><br></td></tr>'% (protocol_color, webprotocol)
		print '<tr><td align="right">Port: </td><td>%s<br></td></tr>'%serverport
		print '<tr><td align="right">Application Version:</td><td>0.4.0<br></td></tr></font>'
	else:
		print '<tr><td align="right">Hostname:</td><td>---<br></td></tr>'
		print '<tr><td align="right">IPv4:</td><td>---<br></td></tr>' 
		print '<tr><td align="right">Protocol: </td><td><font color=\"black\">---<br></td></tr>'
		print '<tr><td align="right">Port: </td><td>---<br></td></tr>'
		print '<tr><td align="right">Application Version:</td><td>0.4.0<br></td></tr></font>'

	
def printsite(modulename,formname_or_cmd,formnotes,formcount):

	if os.path.exists('base.html'):
		basehtml = open('base.html').read().splitlines()

		print 'Content-type: text/html\n\n'

		for each in basehtml: 
			print each #This will print the lines from base.html that is loaded into the FOR LOOP

			#This print the local web server information
			if each == '<!-- StartWebServerInfo -->':

				#This gets and sets the values for the web server
				servervalues = getserverinfo()
				host = servervalues[0]
				ipaddress = servervalues[1]
				webprotocol = servervalues[2]
				port = servervalues[3]
				
				#This will print that infomation for the HTML table in base.html
				printserverinfo(host,ipaddress,webprotocol,port,False)

			#This print the local web server information
			if each == '<!-- StartAppServerInfo -->':
				#This gets and sets the values for the app server 

				if modulename == None:
					printserverinfo(host,ipaddress,webprotocol,port,True)
				else:
					appserverresponse = urllib.urlopen('http://appserver-appdemo:8080/appserverinfo.py')
					appserverhtml = removehtmlheaders(appserverresponse.read())
					print appserverhtml

			if each == '<!-- StartCustom -->':
				#This uses to value passed from the URL to basically set which .py script is used for this section.
				if modulename != None:
					if modulename == 'enterdb':
						enterdbformhtml()
					elif modulename == 'resetdb':
						cleardbformhtml()
					elif modulename == 'commitdb':
						#Here formname_or_cmd is used as the NAME which was entered into the form
						urlstr = 'http://appserver-appdemo:8080/commitdb-app.py?name=%s&notes=%s&count=%s'%(formname_or_cmd,formnotes,formcount)
						appserverresponse = urllib.urlopen(urlstr)
						appserverhtml = removehtmlheaders(appserverresponse.read())
						print appserverhtml
					elif modulename == 'cleardb':
						#Here formname_or_cmd is used as the COMMAND which was entered into the form
						urlstr = 'http://appserver-appdemo:8080/cleardb-app.py?command=%s'%formname_or_cmd
						appserverresponse = urllib.urlopen(urlstr)
						appserverhtml = removehtmlheaders(appserverresponse.read())
						print appserverhtml
					else:
						urlstr = 'http://appserver-appdemo:8080/%s.py'%modulename
						appserverresponse = urllib.urlopen(urlstr)
						appserverhtml = removehtmlheaders(appserverresponse.read())
						print appserverhtml
			
		

		

			
	else:
		print 'ERROR: Base HTML file ', os.path.realpath('base.html'), 'is missing'



				