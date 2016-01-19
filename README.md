# Multi Tiered Web Application 
README for version 0.4.0

##Author:

Brantley Richbourg (brichbourg@gmail.com)

I am a network/systems engineer that is trying to teach myself Python programming.  I am not a developer so please feel free to fork this repo and clean up/improve my code as I am still learning.  

##Information

This is a VERY basic Python based web application I created to be used to demo with SDN environments (Cisco ACI, VMWare NSX, etc).  This application uses a web server Apache2, a "app" server with Apache2 as well, and MySQL as the backend database to function.  The idea is to run the web front end portons of the app on the WEB server with the python scripts.  These scripts will then make HTTP requests to the APP server running Apache2, where those scripts will take the data received and make the SQL calls to the back end MySQL server. 

The idea is to manipulate network policies between Web <--> App<--> MySQL break to application, hence showing the network security policies or contracts work as expected.  

I've also added separate web and app server information displays.  This could be used for demoing load-balancing solutions that are also configured within the SDN application (F5, NSX, Citrix, etc.)

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

###Web Server Installation

* Update Advanced Packaging Tool
	
		sudo apt-get update

* Clone this repo somewhere to your server

		sudo apt-get install git
		git clone https://github.com/brichbourg/Multi-Tier-App-Demo.git

* Install Apache2

		sudo apt-get install apache2

* Install PIP

		sudo apt-get install python-pip

* Install Python Packages

		sudo pip install pymysql

* Run the following commands to make some changes to how Apache operates.

		sudo a2dismod mpm_event
		sudo a2enmod mpm_prefork cgi
		sudo service apache2 restart

*	Edit the `/etc/apache2/sites-enabled/000-default.conf` file with vi or nano (or whatever editor you like)

	Insert the following changes to 000-default.conf under `<VirtualHost *:80>`.  Notice that you are adding Python as a CGI handler AND you are changed the default directory index to index.py instead of index.html.

			<Directory /var/www/html>
		        Options +ExecCGI
		        DirectoryIndex index.py
			</Directory>	
				AddHandler cgi-script .py

* Change the default `DocumentRoot /var/www/html` to `DocumentRoot /var/www/html/appdemo`.  If you don't want to do this, you can always leave it out and access the app via `http://serveraddress/appdemo` if you would rather do that.
	
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

* Now restart the Apache2 service again

		sudo service apache2 restart

* Now `cd` to the directory where you cloned this repo (Multi-Tier-App-Demo) and run the `sitebuild.sh` script

		cd Multi-Tier-App-Demo/
		sudo bash sitebuild.sh

###App Server Installation

For the app server, **FOLLOW THE WEB SERVER DIRECTIONS ABOVE**, but make two changes to have Apache2 listen on port 8080 vs 80.

* Edit `/etc/apache2/ports.conf`:	

	Change `Listen 80` to `Listen 8080`

	The file should look something like this:

		brichbourg@mtwa-app-1:/etc/apache2$ cat ports.conf 
		# If you just change the port or add more ports here, you will likely also
		# have to change the VirtualHost statement in
		# /etc/apache2/sites-enabled/000-default.conf

		Listen 8080

		<IfModule ssl_module>
		        Listen 443
		</IfModule>

		<IfModule mod_gnutls.c>
		        Listen 443
		</IfModule>

		# vim: syntax=apache ts=4 sw=4 sts=4 sr noet

* Now edit the `/etc/apache2/sites-enabled/000-default.conf` again, but only one change needs to be made:

	Change `<VirtualHost *:80>` to `<VirtualHost *:8080>`

* Restart Apache2

		sudo service apache2 restart

### MySQL Server Installation 

This going to be on a separate server from your web/app server.

* Update Advanced Packaging Tool
	
		sudo apt-get update

* Install MySQL
	
		sudo apt-get install mysql-server

	**Make sure you create and remember your MySQL root password!**

* Download the initial SQL file

		wget "https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/sql/create_db_table.sql"

* Now log into your MySQL server as root:

		mysql -u root -p
		<enter your root password>

* Run this command 
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

* Edit `/etc/mysql/my.cnf` to allow for network connections.  Use VI or NANO to edit and change `bind-address = 127.0.0.1` to `bind-address = *`.  This will tell MySQL to listen for connections on port TCP:3306 on all interfaces.
	
		sudo nano /etc/mysql/my.cnf
		.
		.
		.
		<output omitted>
		.
		.
		.
		bind-address	= *

* Restart MySQL

		sudo service mysql restart

* To verify MySQL was configured correct, use netstat -l.  You should see your [serverip]:mysql or [serverip]:3306

		brichbourg@db-1:~$ netstat -l
		Active Internet connections (only servers)
		Proto Recv-Q Send-Q Local Address           Foreign Address         State      
		tcp        0      0 *:ssh                   *:*                     LISTEN     
		tcp        0      0 *:mysql     *:*                     LISTEN     
		tcp6       0      0 [::]:ssh                [::]:*                  LISTEN  


### Configure Bash Menus (Optional)

Here we will configure the bash shell menu scripts that can be configured so that you can use a menu to start and stop services versus having to type them into the CLI manually.  The idea here is this makes demos go faster and smoother.  

* Install Dialog

	This will be used for our Bash menu to control services on the virtual machine.

		sudo apt-get install dialog

* Move Script File

	You will need to copy the correct menu script *depending on the server you are configuring (Web, App or DB)*.  The following example uses the web server.  Note that when we copy it we also change the name and make it a hidden file.

		cp menu_web.sh ~/.menu.sh

	**REMEMBER THAT THE APP SERVER and DB SERVER HAVE DIFFERENT .SH SCRIPTS.  Modify accordingly!**

* Edit ~/.profile

	Now we need to edit the .bashrc file so that this menu will start automatically when the server boots up.

	Add the following string at the end of the file `sudo bash ~/.menu.sh`.  I added sudo so it will prompt you for the root password after you log in.  Ubuntu doesn't allow (to my knowledge) a way to log directly into the system as the root user.


### Final Web/App Server Configuration

Now that we are done configuring the MySQL server, there is one last thing that we need to do in order to get our application working.  To make this easy for people, I've coded the application to use a `/etc/hosts` entry to connect to the MySQL server.  Instead of changing the code (which you can if you would rather), I have just hard coded the Python scripts to connect to `dbserver-appdemo`.

You need to edit your `/etc/hosts` files and add an entry to point to the IP address of **YOUR** App Server and MySQL server.  If you IP addresses are entered incorrectly here, the app will not function correctly.

* On the Web Server add this to `/etc/hosts`:
			
			192.168.1.101	appserver-appdemo

* On the App Server add this to `/etc/hosts`:
			
			192.168.1.102	dbserver-appdemo

Now you just need to replace the logo `logo.jpg` to the directory `/var/www/html/appdemo` so you have a picture at the top of your app if you don't like the one I provided.



