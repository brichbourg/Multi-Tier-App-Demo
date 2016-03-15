#!/bin/bash

##
## This script modifies an Apache2 configuration file and adds the necessary configuration to 
## enable the Mutli-Tier Application.
##

##
## Written by Luis Chanu
##

##
## Script Usage:
##	cd /etc/apache2/sites-enabled
##	bash a2appdemo 000-default.conf
##

##
## Detailed information about this script
## ======================================
##
## This modifies the Apache2 configuration file by modifying it to include the following:
##
##	DocumentRoot /var/www/html/appdemo
##
##	<Directory /var/www/html>
##		Options +ExecCGI
##		DirectoryIndex index.py
##	</Directory>
##	AddHandler cgi-script .py
##
##
## If the configuration file includes SSL certificates, they get updated to use the MTA-Web files.
##


##
## Known Limitations
## =================
## 1) The argument to the a2appdemo.sh should be a single filename, and NOT include any path.
##

##
## Change Log
## ==========
##
## 2016-03-13
## 1) Initial version of the file.
## 2) Added support to update SSL support in the same script.
##

#####################################################################################################

##
##Check arguments to see if filename was entered by the user
##
if [ "$#" -ne 1 ]; then
	echo "Usage: a2appdemo <Apache2-config-file-to-modify>"
	exit
fi


##
##Notify user what is about to happen
##
echo "Modifying Apache2 " $1 " configuration file..."


##
##Modify file passed in and temporarilly store it in -new file
##
sed 's_/var/www/html_/var/www/html/appdemo_' $1 | sed '/DocumentRoot/ a \'\\n\\t'<Directory  /var/www/html>\n'\\t\\t'Options +ExecCGI\n'\\t\\t'DirectoryIndex  index.py\n'\\t'</Directory>\n'\\t'AddHandler  cgi-script .py\n' | sed '/ssl-cert-snakeoil.pem/ c \'\\t\\t'SSLCertificateFile'\\t'/etc/ssl/certs/MTA-Web.pem' | sed '/ssl-cert-snakeoil.key/ c \'\\t\\t'SSLCertificateKeyFile'\\t'/etc/ssl/private/MTA-Web.key' > /tmp/$1_new


##
##Rotate Files
##
echo "Original " $1 "file copied to "$1"_ORIG"
rm $1_ORIG
cp $1 $1_ORIG
cp /tmp/$1_new $1
rm /tmp/$1_new

