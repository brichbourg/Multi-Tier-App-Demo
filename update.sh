#!/bin/bash

echo -e "We are going to update the site with the latest code from GitHub, press ENTER key to continue, or CTRL-C to quit"
read key
sudo cd ~/Multi-Tier-App-Demo
sudo git pull 
sudo cp html/* /var/www/html/appdemo/
sudo cp scripts/* /var/www/html/appdemo/

echo "Update complete!"

