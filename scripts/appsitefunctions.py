#!/usr/bin/python
import os.path
import cgi
# Turn on debug mode.
import cgitb
cgitb.enable()


def loadbasehtml(modulename):

	if os.path.exists('base.html'):
		basehtml = open('base.html').read().splitlines()

		print 'Content-type: text/html\n\n'
		for each in basehtml: 

			#This print the local web server information
			if each == '<!-- StartServerInfo -->':
				# print "START SERVER IF STATEMENT" #db
				import server_info 
			#This will call the script to generate the contents or the page that is unique.
			if each == '<!-- StartCustom -->':
				#This uses to value passed from the URL to basically set which .py script is used for this section.
				if modulename != None:
					module = __import__(modulename)	

			print each

		

			
	else:
		print 'ERROR: Base HTML file ', os.path.realpath('base.html'), 'is missing'


# def main():
# 	#this was for debugging only
# 	# name=None
# 	# loadbasehtml(name)

# if __name__ == "__main__":
# 	main()


				