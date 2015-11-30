#!/usr/bin/python

import appsitefunctions
import cgi

servervalues = appsitefunctions.getserverinfo()

host = servervalues[0]
print host, 'host'
ipaddress = servervalues[1]
print ipaddress, 'ipaddress'
webprotocol = servervalues[2]
print webprotocol, "webprotocol"
port = servervalues[3]
print port, 'port'

appsitefunctions.printserverinfo(host,ipaddress,webprotocol,port)
