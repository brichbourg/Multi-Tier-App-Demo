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
	
def printserverinfo(hostname,ipaddress,webprotocol,serverport):

	protocol_color = setcolor(webprotocol)
	print '<tr><td align="right">Hostname:</td><td>%s<br></td></tr>'%hostname
	print '<tr><td align="right">IPv4:</td><td>%s<br></td></tr>' %ipaddress
	print '<tr><td align="right">Protocol: </td><td><B><font color=\"%s\">%s</font></B><br></td></tr>'% (protocol_color, webprotocol)
	print '<tr><td align="right">Port: </td><td>%s</font><br></td></tr>'%serverport
	print '<tr><td align="right">Application Version:</td><td>0.4.0 BETA</font><br></td></tr></font>'

	
def printsite(modulename):

	if os.path.exists('base.html'):
		basehtml = open('base.html').read().splitlines()

		print 'Content-type: text/html\n\n'

		for each in basehtml: 
			print each #This will print the line from base.html that is loaded into the FOR LOOP

			#This print the local web server information
			if each == '<!-- StartWebServerInfo -->':

				#This gets and sets the values for the web server
				servervalues = getserverinfo()
				host = servervalues[0]
				ipaddress = servervalues[1]
				webprotocol = servervalues[2]
				port = servervalues[3]
				
				#This will print that infomation for the HTML table in base.html
				printserverinfo(host,ipaddress,webprotocol,port)

			#This print the local web server information
			if each == '<!-- StartAppServerInfo -->':
				#This gets and sets the values for the app server 

				appserverdata = urllib.urlopen('http://appserver-appdemo/appserverinfo.py')

				
			#This will call the script to generate the contents or the page that is unique.
			if each == '<!-- StartCustom -->':
				#This uses to value passed from the URL to basically set which .py script is used for this section.
				if modulename != None:
					module = __import__(modulename)	

			
			
		

		

			
	else:
		print 'ERROR: Base HTML file ', os.path.realpath('base.html'), 'is missing'



				