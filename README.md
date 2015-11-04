# Demo Tiered Web Application

Version 0.1 

##Author:

Brantley Richbourg (brichbourg@gmail.com)

I am a network/systems engineer that is trying to teach myself Python programming.  I am not a developer so please feel free to fork this repo and clean up/improve my code as I am still learning.  

##Information

This is a VERY basic Python based web application I created to be used to demo with SDN environments (Cisco ACI, VMWare NSX, etc).  This application uses the web server Apache2 and MySQL as the backend database to function.  The idea is to run Apache2 with the python scripts and MySQL on separate servers and then manipulate network policies between Web/App Server and DB server the break to application.

The functions created allow a user to view contents, add records to, and erase the contents of a MySQL database. 

This application is provided "as-is".

Here are the versions of the systems I used when creating it:

* Ubuntu Linux 14.04.3 LTS
* Python 2.7.6
* Apache 2.4.7 
* MySQL Ver 14.14 Distrib 5.5.46

NOTE: These instructions are to be used on "clean" server installations.  Use with existing Apache2 and MySQL systems as your own risk!!!

## Web Server Build

###Software Installation

Clone this repo somewhere to your server

	sudo apt-get install git
	git clone https://github.com/brichbourg/Multi-Tier-App-Demo.git

Install Apache2

	sudo apt-get install apache2

Install PIP

	sudo apt-get install python-pip

Install Python Packages

	sudo pip install pymysql

###Server Modifications

	sudo a2dismod mpm_event
	sudo a2enmod mpm_prefork cgi
	sudo service apache2 restart

Edit the the following file with vi or nano (or whatever editor you like)

	/etc/apache2/sites-enabled/000-default.conf

Insert the following changes to 000-default.conf

* Options +ExecCGI
* AddHandler cgi-script .py
	
Example 000-default.conf with the comments removed:

	<VirtualHost *:80>
	<Directory /var/www/html>
    		Options +ExecCGI
    		DirectoryIndex index.html
	</Directory>
	AddHandler cgi-script .py

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	</VirtualHost>

Now restart the Apache2 service again

	sudo service apache2 restart

## MySQL Server Installation 
## (On a separate server from the web server)

Install MySQL
	
	sudo apt-get install mysql-server

***Make sure you create and remember your MySQL root password!

Download the initial SQL file

	wget "https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/sql/create_db_table.sql"

Now log into your MySQL server as root:

	mysql -u root -p
	<enter your root password>

Run this command 
NOTE: The example below assumes you ran the wget command from your home directory.  Modify as needed.

	mysql> source ~/create_db_table.sql;

Here is the SQL code being injected


	CREATE DATABASE `appdemo`;
	USE `appdemo`;
	CREATE TABLE `demodata` (
	`id` INTEGER NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(100),
	`notes` TEXT,
	`timestamp` TIMESTAMP,
	PRIMARY KEY (`id`),
	KEY (`name`)
	);

	CREATE TABLE `demodata_erase_log` (
	`id` INTEGER NOT NULL AUTO_INCREMENT,
	`timestamp` TIMESTAMP,
	PRIMARY KEY (`id`),
	KEY (`timestamp`)
	);

##Usage





