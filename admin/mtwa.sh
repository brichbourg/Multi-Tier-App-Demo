#!/bin/bash
#install-mtwa.sh - version 0.1.0
#
#Written by Brantley Richbourg with contributions from Luis Chanu
#
#This script is still being built, so the README has not been updated yet to reflect installing with this vs manually doing everything.
#Define the functions that will run the commands needed to install the components
function copysite {
    cp /opt/Multi-Tier-App-Demo/html/* /var/www/html/appdemo/
    cp /opt/Multi-Tier-App-Demo/scripts/* /var/www/html/appdemo/
    echo "MTWA Scripts and HTML copied to /var/www/html/appdemo"
 }

function createsite {
    mkdir /var/www/html/appdemo
    copysite
}

function installwebserver {
	echo Install Web Server Function
	apt-get -q -y update
	apt-get -q -y install dialog apache2 python-pip 
	pip install pymysql 

	a2dismod mpm_event
	a2enmod mpm_prefork cgi
	service apache2 restart
    createsite 
 }
 
function installappserver {
 	echo Install App Server Function
 	apt-get -q -y update
	apt-get -q -y install dialog apache2 python-pip 
	pip install pymysql 

	a2dismod mpm_event
	a2enmod mpm_prefork cgi
	service apache2 restart
    createsite
 }

function installdbserver {
 	echo Install Database Server Function
 	apt-get -q -y update
	apt-get -q -y install dialog mysql-server


 }

function updatecode {
 	echo Update Code Function
 	cd /opt/Multi-Tier-App-Demo
 	git pull
    copysite
 }



echo "This script will install MTWA (Multi-Tier Web Application) to this server."
echo "Please enter the server role for this machine:"

# Here is the menu for the installation script
options=("Install Web Server" "Install Application Server" "Install Database Server" "Update Code From GitHub" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Install Web Server")
            installwebserver
            ;;
        "Install Application Server")
            installappserver
            ;;
        "Install Database Server")
            installdbserver
            ;;
        "Update Code From GitHub")
            updatecode
            ;;
        "Quit")
            break
            ;;
        *) echo invalid option;;
    esac
done
