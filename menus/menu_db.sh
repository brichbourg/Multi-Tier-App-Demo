	
#!/bin/bash
# Bash Menu Script to use on the MTWA virtual machines to start and stop services during demos.
##!/bin/bash

HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=4
BACKTITLE="Multi-Tier Web Application"
TITLE="Database Server Control Center"
MENU="Choose one of the following options:"

OPTIONS=(1 "Start MySQL"
         2 "Stop MySQL"
         3 "MySQL Server Status"
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
            echo "Starting MySQL Server"
            sudo service mysql start
            sudo service mysql status
            read -p "Press any key to continue"
            bash menu_db.sh
            ;;
        2)
            echo "Stopping MySQL Server"
            sudo service mysql stop
            sudo service mysql status
            read -p "Press any key to continue"
            bash menu_db.sh
            ;;
        3)
            sudo service mysql status
            read -p "Press any key to continue"
            bash menu_db.sh
            ;;
        4)
            
            ;;
esac