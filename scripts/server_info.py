#!/usr/bin/python

import socket

#This code establishes a TCP connection to the backend MySQL server to get the host's IP address.  This assumes the user has modified /etc/hosts as per the README
#If the MySQL severs is on the same host at the web server, then this will display whatever value you entered into /etc/hosts for dbserver-appdemo
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(("dbserver-appdemo",3306))
ipaddress=(sock.getsockname()[0])
sock.close()

#This get the hostname as defined in /etc/hostname
hostname = (socket.gethostname())

#This prints the HTML portion needed when this scripts is imported into another script printing HTML code.
print '<tr><td align="right">Web Server:</td><td>', hostname , '<br></td></tr>'
print '<tr><td align="right">IPv4:</td><td>' , ipaddress , '<br></td></tr>'
print '<tr><td align="right">Protocol: </td><td>To Be Developed</font><br></td></tr>'

