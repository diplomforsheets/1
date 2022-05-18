#!/bin/bash
var=0
ls|egrep temp\[0-9]\+|xargs rm -rf
while read LINE
do
        if [[ $LINE =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        let var=$var+1
        echo "$LINE"
        mkdir "temp${var}"
        ansible -i hosts.lin -m shell -a 'cat /sys/class/net/*/address' "$LINE" | sed '/SUCCESS/d' |grep -v 00:00:00:00:00:00 > "temp${var}/1" #MAC_Address
        echo "$LINE" > "temp${var}/2"   #IP_addres
        ansible -i hosts.lin -m shell -a 'uname -somn' "$LINE" | sed '/SUCCESS/d' > "temp${var}/3"      #OS_bild_kernel
        ansible -i hosts.lin -m shell -a 'lscpu | grep "Model name"'  "$LINE" | sed '/SUCCESS/d' > "temp${var}/4"       #PROCESOR
        ansible -i hosts.lin -m shell -a 'lspci | grep -E "VGA|3D"'  "$LINE" | sed '/SUCCESS/d' > "temp${var}/5"        #grafic_card
        ansible -i hosts.lin -m shell -a 'cat /proc/meminfo |grep MemTotal'  "$LINE" | sed '/SUCCESS/d' > "temp${var}/6" #operativ_memory
        ansible -i hosts.lin -m shell -a 'lshw -C memory |grep bank:0 -A 25 |grep description |grep -v empty'  "$LINE" | sed '/SUCCESS/d' > "temp${var}/7" #operativ_memory_description
        ansible -i hosts.lin -m shell -a 'lshw -class disk | grep product | head -n1'  "$LINE" | sed '/SUCCESS/d' > "temp${var}/8" #hard_drive
        ansible -i hosts.lin -m shell -a ' dmidecode |grep "BIOS Information" -A 10 | grep Vendor -A 1'  "$LINE" | sed '/SUCCESS/d' |awk '{print }' ORS=' ' | awk '{print}' > "temp${var}/9" #BIOS
        ansible -i hosts.lin -m shell -a 'dmidecode |grep "Base Board" -A 10 |grep Manufacturer -A 1' "$LINE" | sed '/SUCCESS/d'  |awk '{print }' ORS=' ' | awk '{print}' > "temp${var}/10" #Mother_board
        ansible -i hosts.lin -m shell -a ' lshw | grep network -A 3 | grep product'  "$LINE" | sed '/SUCCESS/d' > "temp${var}/11" #network_card
        ansible -i hosts.lin -m shell -a 'lshw'  "$LINE" | sed '/SUCCESS/d' | awk -v A=-1 '/DISABLED/ { A = 18 } A-- >= 0 {next } 1' | awk -v A=-1 '/UNCLAIMED/ { A = 4 } A-- >= 0 {next } 1' > "all${var}.txt"
        fi
done < hosts.lin
while read LINE
do
        if [[ $LINE =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        let var=$var+1
        echo "$LINE"
        mkdir "temp${var}"
        ansible -i hosts.win -m win_command -a "ipconfig /all" " $LINE" | sed '/SUCCESS/d' | grep "Physical Address"| egrep -o ' [0-9A-F][0-9A-F]-[0-9A-F][0-9A-F]-[0-9A-F][0-9A-F]-[0-9A-F][0-9A-F]-[0-9A-F][0-9A-F]-[0-9A-F][0-9A-F]' |grep -v "00:00:00:00:00:00" > "temp${var}/1" #MAC_Address
        echo "$LINE" > "temp${var}/2"   #IP_addres
        ansible -i hosts.win -m win_command -a "systeminfo" " $LINE" | sed '/SUCCESS/d' |grep "Host Name:" -A 2 |tr -s ' ' > "temp${var}/3"      #OS_bild_kernel
        ansible -i hosts.win -m win_command -a "systeminfo" " $LINE" | sed '/SUCCESS/d' |grep "Processor(s):" -A 10 | grep -e [\[][0-9][0-9]\]: > "temp${var}/4"       #PROCESOR
        ansible -i hosts.win -m win_command -a "wmic path win32_VideoController get name" " $LINE" | egrep -v -e "^$" -e "Name" -e "SUCCESS" > "temp${var}/5.dos"        #grafic_card
        dos2unix -q "temp${var}/5.dos"
        sed '/^$/d' temp${var}/5.dos >  "temp${var}/5"
        ansible -i hosts.win -m win_command -a "systeminfo" " $LINE" | sed '/SUCCESS/d' |grep "Total Physical Memory"|egrep -v -e "^$" > "temp${var}/6" #operativ_memory
        ansible -i hosts.win -m win_command -a "wmic MEMORYCHIP get DeviceLocator, MemoryType, Capacity, Speed, CreationClassName" " $LINE" | egrep -v -e "^$" -e "SUCCESS" > "temp${var}/7.dos" #operativ_memory_description
        dos2unix -q "temp${var}/7.dos"
        sed '/^$/d' temp${var}/7.dos >  "temp${var}/7"
        ansible -i hosts.win -m win_command -a "wmic diskdrive get model,serialNumber,size,mediaType" " $LINE" | egrep -v -e "^$" -e "SUCCESS" -e "MediaType" > "temp${var}/8.dos" #hard_drive
        dos2unix -q "temp${var}/8.dos"
        sed '/^$/d' temp${var}/8.dos >  "temp${var}/8"
        ansible -i hosts.win -m win_command -a "systeminfo" " $LINE" | sed '/SUCCESS/d' |grep "BIOS Version:"  > "temp${var}/9" #BIOS
        ansible -i hosts.win -m win_command -a "wmic baseboard get product,Manufacturer,serialnumber" " $LINE" |grep -v -e "Manufacturer" -e "SUCCESS" -e "^$" > "temp${var}/10.dos" #Mother_board
        dos2unix -q "temp${var}/10.dos"
        sed '/^$/d' temp${var}/10.dos >  "temp${var}/10"
        ansible -i hosts.win -m win_command -a "systeminfo" " $LINE" | sed '/SUCCESS/d' |grep "Network Card(s):" -A 50 | grep -e [\[][0-9][0-9]\]:[" "][A-Z] > "temp${var}/11" #network_card
        ansible -i hosts.win -m win_command -a "systeminfo" " $LINE" | sed '/SUCCESS/d' > "all${var}.txt"
        fi
done <hosts.win
