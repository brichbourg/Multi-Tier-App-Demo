# Multi Tiered Web Application 

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

##Screenshots

I think that you will find using this application to be pretty self explanatory, so instead of describing everything, I decided to include some screenshots so people can see what it looks like.

###Main Menu: 
![alt text](https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/screenshots/mainmenu.png "Main Menu")

###Enter Data: 
![alt text](https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/screenshots/enterdata.png "Enter Data")

###Commit Data 
![alt text](https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/screenshots/commitdata.png "Commit Data")

###View Data
![alt text](https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/screenshots/viewdata.png "View Data")

###Erase Data
![alt text](https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/screenshots/cleardata.png "Erase Data")


## Installation Instructions

###Web/App Server Installation

Clone this repo somewhere to your server

	sudo apt-get install git
	git clone https://github.com/brichbourg/Multi-Tier-App-Demo.git

Install Apache2

	sudo apt-get install apache2

Install PIP

	sudo apt-get install python-pip

Install Python Packages

	sudo pip install pymysql

Run the following commands to make some changes to how Apache operates.

	sudo a2dismod mpm_event
	sudo a2enmod mpm_prefork cgi
	sudo service apache2 restart

Edit the `/etc/apache2/sites-enabled/000-default.conf` file with vi or nano (or whatever editor you like)

Insert the following changes to 000-default.conf under `<VirtualHost *:80>`.  Notice that you are adding Python as a CGI handler AND you are changed the default directory index to index.py instead of index.html.

	<Directory /var/www/html>
	        Options +ExecCGI
	        DirectoryIndex index.py
	</Directory>
	AddHandler cgi-script .py

Change the default `DocumentRoot /var/www/html` to `DocumentRoot /var/www/html/appdemo`.  If you don't want to do this, you can always leave it out and access the app via `http://serveraddress/appdemo` if you would rather do that.
	
Here is what the whole `000-default.conf` file should look like (with the #comments removed):

	<VirtualHost *:80>
	<Directory /var/www/html>
    		Options +ExecCGI
    		DirectoryIndex index.py
	</Directory>
	AddHandler cgi-script .py

	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html/appdemo

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	</VirtualHost>

Now restart the Apache2 service again

	sudo service apache2 restart

Now `cd` to the directory where you cloned this repo (Multi-Tier-App-Demo) and run the `sitebuild.sh` script

	cd Multi-Tier-App-Demo/
	sudo bash sitebuild.sh


### MySQL Server Installation 

This going to be on a separate server from your web/app server.

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

Here is the SQL code being injected:


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

	CREATE USER 'appdemo'@'%' IDENTIFIED BY 'appdemo';
	GRANT ALL PRIVILEGES ON appdemo.* to 'appdemo'@'%' WITH GRANT OPTION;

Edit `/etc/mysql/my.cnf` to allow for network connections.  Use VI or NANO to edit and change `bind-address = 127.0.0.1` to `bind-address = *`.  This will tell MySQL to listen for connections on port TCP:3306 on all interfaces.
	
	sudo nano /etc/mysql/my.cnf
	.
	.
	.
	<output omitted>
	.
	.
	.
	bind-address	= *

Restart MySQL

	sudo service mysql restart

To verify MySQL was configured correct, use netstat -l.  You should see your [serverip]:mysql or [serverip]:3306

	brichbourg@db-1:~$ netstat -l
	Active Internet connections (only servers)
	Proto Recv-Q Send-Q Local Address           Foreign Address         State      
	tcp        0      0 *:ssh                   *:*                     LISTEN     
	tcp        0      0 *:mysql     *:*                     LISTEN     
	tcp6       0      0 [::]:ssh                [::]:*                  LISTEN  


### Final Web Server Configuration

Now that we are done configuring the MySQL server, there is one last thing that we need to do in order to get our application working.  To make this easy for people, I've coded the application to use a `/etc/hosts` entry to connect to the MySQL server.  Instead of changing the code (which you can if you would rather), I have just hard coded the Python scripts to connect to `dbserver-appdemo`.

You need to edit your `/etc/hosts` files and add an entry to point to the IP address of **your** MySQL server.

	
	192.168.1.100       dbserver-appdemo

Now you just need to replace the logo `logo.jpg` to the directory `/var/www/html/appdemo` so you have a picture at the top of your app if you don't like the one I provided.



