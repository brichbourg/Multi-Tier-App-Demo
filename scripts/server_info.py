#!/usr/bin/python

#This is a "module" script.  This is loaded by index.py to print the local server information.

import socket
import cgi
import os

def getserverinfo(param_name):

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

#This code establishes a TCP connection to the app server to get the host's IP address.  This assumes the user has modified /etc/hosts as per the README
#If the app server is on the same host at the web server, then this will display whatever value you entered into /etc/hosts for appserver-appdemo
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("appserver-appdemo",80))
ipaddress=(sock.getsockname()[0])
sock.close()

#This get the hostname as defined in /etc/hostname
hostname = (socket.gethostname())
apphostname = 'TBD'
#Use OS environment variables gather information
serverprotocol = str.upper(getserverinfo('REQUEST_SCHEME'))
# serverprotocol = 'HTTPS'
protocol_color = setcolor(serverprotocol)
serverport = getserverinfo('SERVER_PORT')

#IF YOU WANT TO FIGURE OUT WHAT VARIABLES CAN BE USED, UNCOMMENT THE NEXT LINE TO ADD OTHER INFORMATION AND REFRESH THE WEBPAGE
# cgi.test() 

print '<tr><td align="right">OLD MODULE</td><td>OLD MODULE DON\'T USE<br></td></tr>'

#This prints the HTML portion needed when this scripts is imported into another script printing HTML code.
# print '<tr><td align="right">Web Server:</td><td>%s<br></td></tr>'%hostname
# print '<tr><td align="right">IPv4:</td><td>%s<br></td></tr>' %ipaddress
# print '<tr><td align="right">Protocol: </td><td><B><font color=\"%s\">%s</font></B><br></td></tr>'% (protocol_color, serverprotocol)
# print '<tr><td align="right">Port: </td><td>%s</font><br></td></tr>'%serverport
# print '<tr><td align="right">Application Version:</td><td>0.4.0 BETA</font><br></td></tr></font>'
# print '<tr><td align="right">App Server:</td><td>%s<br></td></tr>'%apphostname
# print '<tr><td align="right">IPv4:</td><td>%s<br></td></tr>' %ipaddress
# print '<tr><td align="right">Protocol: </td><td><B><font color=\"%s\">%s</font></B><br></td></tr>'% (protocol_color, serverprotocol)
# print '<tr><td align="right">Port: </td><td>%s</font><br></td></tr>'%serverport
# print '<tr><td align="right">Application Version:</td><td>0.4.0 BETA</font><br></td></tr></font>'

#Returns a list of values


	





