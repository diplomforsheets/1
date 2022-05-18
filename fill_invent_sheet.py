import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import os.path
from pathlib import Path
import os
import re
import json
from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
CREDENTIALS_FILE = 'diplosheets-4490f33dbc26.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) 
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем ра-боту с таблицами и 4 версию API
with open('.proect_all_spreadsheet', 'r') as f:
    lines = f.read().splitlines()
    last_line = lines[-1]
eject_id=(last_line).split(' ')
spreadsheetId =  eject_id[0]
results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = { "valueInputOption": "USER_ENTERED", "data": [ {"range": "List_of_all_inventarizateon!A1:A15", "majorDimension": "ROWS", "values": [  ["MAC_ADDRESS"], ["IP_addres"], ["OS_bild_kernel"], ["Procesor"],  ["Grafic_card"],  ["Amount_of_RAM"],  ["RAM_description"], ["Hard_drive"], ["BIOS"], ["Mother_board"], ["Network_card"], [""], [""],  ["big_info"] , ["big_info"]]}]}).execute()
count = 1
while os.path.exists("temp"+str(count)):
        var=1
        while os.path.isfile("temp"+str(count)+"/"+str(var)):
                file = open("temp"+str(count)+"/"+str(var), "r")
                s=file.read()
                s = re.sub(" +", " ", s)
results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {"valueInputOption": "USER_ENTERED","data": [{"range": "List_of_all_inventarizateon!"+chr(65+count)+str(var)+":"+chr(65+count)+str(var),"majorDimension": "ROWS",  "values": [  [s]]}]}).execute()
                var+=1
                file.close()
        count+=1
count = 1
def get_grid_id(service):
    response = service.spreadsheets().get(spreadsheetId=spreadsheetId, includeGridData=True).execute()
    return response['sheets'][0]['properties']['sheetId']
def sheets_update(sheets_service, grid_id):
    body = {"requests": [{"autoResizeDimensions": {"dimensions": {"sheetId": grid_id,  "dimension": "COLUMNS"}   }}  ]}
    response = sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()
sheets_update(service, get_grid_id(service))
while os.path.isfile("all"+str(count)+".txt"):
    file = open("all"+str(count)+".txt", "r")
    lshw = file.read()
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {"valueInputOption": "USER_ENTERED","data": [{"range": "List_of_all_inventarizateon!"+chr(65+count)+"15:"+chr(65+count)+"15","majorDimension": "ROWS","values": [[lshw]]}]}).execute()
    count+=1
    file.close()
