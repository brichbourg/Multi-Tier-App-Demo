	
#!/bin/bash
# Bash Menu Script to use on the MTWA virtual machines to start and stop services during demos.
# Copy to home folder and rename to .menu.sh
##!/bin/bash

HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="Multi-Tier Web Application"
TITLE="App Server Control Center"
MENU="Choose one of the following options:"

OPTIONS=(1 "Start App Server"
         2 "Stop App Server"
         3 "App ServerStatus"
         4 "Exit to CLI")

CHOICE=$(dialog --clear \
                --backtitle "$BACKTITLE" \
                --title "$TITLE" \
                --menu "$MENU" \
                $HEIGHT $WIDTH $CHOICE_HEIGHT \
                "${OPTIONS[@]}" \
                2>&1 >/dev/tty)

clear
case $CHOICE in
        1)
            echo "Starting Apache Server"
            sudo service apache2 start
            sudo service apache2 status
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        2)
            echo "Stopping Apache Server"
            sudo service apache2 stop
            sudo service apache2 status
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        3)
            sudo service apache2 status
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        4)
            
            ;;
esac