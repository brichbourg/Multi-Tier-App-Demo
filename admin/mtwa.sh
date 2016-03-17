#!/bin/bash
#install-mtwa.sh - version 0.1.1
#
#Written by Brantley Richbourg with contributions from Luis Chanu
#
#This script is still being built, so the README has not been updated yet to reflect installing with this vs manually doing everything.
#Define the functions that will run the commands needed to install the components

#This function is used to display the version of the app when the script is first run.  I placed it in a function so it was at the top of the file.
function appversion {
    echo "Management Script Version 0.1.1"
    echo " "
}

function copysite {
    cp /opt/Multi-Tier-App-Demo/html/* /var/www/html/appdemo/
    cp /opt/Multi-Tier-App-Demo/scripts/* /var/www/html/appdemo/
    echo "MTWA Scripts and HTML copied to /var/www/html/appdemo, press RETURN to continue"
 }

function createsite {
    mkdir /var/www/html/appdemo
    copysite
}

#Installed the Apache and other modules needed for the web server.
function installwebserver {
	echo Installing the web server applications and services
	apt-get -q -y update
	apt-get -q -y install dialog apache2 python-pip 
	pip install pymysql 

	a2dismod mpm_event
	a2enmod mpm_prefork cgi
	service apache2 restart
    createsite 
    echo "Install Complete, press RETURN to continue."
 }
 
#Installs the app server functionality, which is currectly the same as web (to be developed)
function installappserver {
 	echo Installing the app server applications and services
 	apt-get -q -y update
	apt-get -q -y install dialog apache2 python-pip 
	pip install pymysql 

	a2dismod mpm_event
	a2enmod mpm_prefork cgi
	service apache2 restart
    createsite
    echo "Install Complete, press RETURN to continue."
 }

#Install the database functionality (MySQL, etc)
function installdbserver {
 	echo Installing the MySQL server applications and services
 	apt-get -q -y update
	apt-get -q -y install dialog mysql-server
    echo "Install Complete, press RETURN to continue."
 }

#This function will pull the latest scripts, etc from the GitHub repo.  This will pull whatever branch is configured (usually master)
function updatecode {
 	echo "Press RETURN to update the application to the latest version, or ctrl-c to exit"
    read 
 	cd /opt/Multi-Tier-App-Demo
 	git pull
    copysite
    echo "Site Updated, press RETURN to continue."
 }

function configurehttp {
    echo This feature is currently under development.
}

function configurehttps {
    echo This feature is currently under development.
}

#Start of the main section of the script
echo " "
echo "Welcome to Multi-Tier Web App (MTWA) " 

#Call the function at the top of the script to display the version number of this script.
appversion

# Here is the menu for the installation script
options=("Install" "Configure"  "Update" "Quit")
optionsprompt='Please enter your choice: '

sub1=("Web" "App" "DB" "Back")
sub1prompt='Please enter what role you want to install: '

sub2=("Configure HTTP" "Configure HTTPS" "Back")
sub2prompt='Please enter your choice: '

PS3=$optionsprompt
select opt in "${options[@]}"
do
    case $opt in
        "Install")

            echo "Installation Options"
            PS3=$sub1prompt
            select sub1opt in "${sub1[@]}"  
            do
                case $sub1opt in
                    "Web")
                        echo "Installing Web Server"
                        installwebserver
                        ;;
                    "App")
                        echo "Installing App Server"
                        installappserver
                        ;;
                    "DB")
                        echo "Installing DB Server"
                        installdbserver
                        ;;  
                    "Back")
                        echo "Going back to previous menu; press ENTER to display options"
                        break
                        ;;                      
                 esac
            done
            ;;

        "Configure")
            echo "Configuration Options"
            PS3=$sub2prompt
            select sub2opt in "${sub2[@]}"
            do
                case $sub2opt in
                    "Configure HTTP")
                        echo "Configuring HTTP"
                        configurehttp
                        ;;
                    "Configure HTTPS")
                        echo "Configuring HTTPS"
                        configurehttps
                        ;;
                    "Back")
                        echo "Going back to previous menu; press ENTER to display options"
                        break
                        ;;                         
                 esac
            done
            ;;
        "Update")
            echo "Update Code From GitHub Repository"
            updatecode
            ;;

        "Quit")
            break
            ;;            
        *) echo invalid option;;
    esac
done
