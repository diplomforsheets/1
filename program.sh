#!/bin/bash
echo "start of $0"
date
FILE=.proect_all_spreadsheet
if test -f "$FILE"; then
    echo "new inwentarization"
else
echo "new progect"
python3 new_spreadsheet.py
fi
python3 new_spreadsheet.py
python3 fill_main.py
rm -rf hosts.*
./OS_sort
./ansible_work.sh
python3 fill_invent_sheet.py
DIRECTORY="./temp.check1/"
if [[ -d "${DIRECTORY}" && ! -L "${DIRECTORY}" ]]; then
python3 basic_check.py
else
i=1
while test -d "./temp$i/"
do
cp -r "temp$i" "temp.check$i"
let i=i+1
done
fi
date
echo "end of $0"
