#!/bin/bash

echo -e "We are going to copy the files over to Apache, press any key to continue, or CTRL-C to quit"
read key
sudo mkdir /var/www/html/appdemo
sudo cp html/* /var/www/html/appdemo/
sudo cp scripts/* /var/www/html/appdemo/

echo "Completed, please go to http://<serveraddress>/appdemo to test the application"

