	
#!/bin/bash
# Bash Menu Script to use on the MTWA virtual machines to start and stop services during demos.
##!/bin/bash

HEIGHT=15
WIDTH=40
CHOICE_HEIGHT=8
BACKTITLE="Multi-Tier Web Application"
TITLE="Web Server Control Center"
MENU="Choose one of the following options:"

OPTIONS=(1 "Start Apache"
         2 "Stop Apache"
         3 "Apache Server Status"
         4 "Block HTTP (IPTABLES)"
         5 "Block HTTPS (IPTABLES)"
         6 "Clear IPTABLES"
         7 "Show IPTABLES Rules"
         8 "Exit to CLI")

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
            echo "Blocking HTTP (IPTABLES)"
            sudo iptables -A INPUT -p tcp --dport http -j DROP
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        5)
            echo "Blocking HTTPS (IPTABLES)"
            sudo iptables -A INPUT -p tcp --dport https -j DROP
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        6)
            echo "Clearing IPTABLES rules"
            sudo iptables -F
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        7)
            echo "Showing IPTABLES rules"
            sudo iptables -L
            read -p "Press any key to continue"
            bash .menu.sh
            ;;
        8)
            
            ;;
esac