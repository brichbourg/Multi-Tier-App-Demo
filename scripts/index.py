#!/usr/bin/python
import os.path
import cgi
import appsitefunctions

# Turn on debug mode.
import cgitb
cgitb.enable()

#This will figure out what module to call based on the URL passed.  /index.py?module=viewdb for example
form = cgi.FieldStorage()
modulename = form.getvalue('module')

#This will call the fucntion to loab the base.html file for the site.
appsitefunctions.loadbasehtml(modulename)
