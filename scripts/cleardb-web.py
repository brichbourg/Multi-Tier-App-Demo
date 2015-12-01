#!/usr/bin/python
import os.path
import cgi
import appsitefunctions

# Turn on debug mode.
import cgitb
cgitb.enable()

#This will figure out what module to call based on the URL passed.  /index.py?module=viewdb for example
form = cgi.FieldStorage()
name = form.getvalue('command')
# print form, "<!-- (DEBUG) -->"

#This will call the fucntion to loab the base.html file for the site.
#I am using the "name" variable to pass the value of the command entered into the site.  Name is used in the enterdb functionality. 
appsitefunctions.printsite('cleardb',name,None,None)