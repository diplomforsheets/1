import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import os.path
from pathlib import Path
import os
import json
from apiclient import discovery
from apiclient.http import MediaFileUpload
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
CREDENTIALS_FILE = 'diplosheets-4490f33dbc26.json'  
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) 
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth
file = open(".proect_all_spreadsheet", "r")
first_lint=(file.readline()).split(' ')
spreadsheetId =  first_lint[0]
file.close()
results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = { "valueInputOption": "USER_ENTERED", "data": [{"range": "List_of_all_inventarizateon!A1:C1","majorDimension": "COLUMNS","values": [ ["SHEET_№"] ,[ "LINK"] ,[ "TIME_OF_CREATION"]]}  ]}).execute()
f = open(".proect_all_spreadsheet", "r")
count_of_lines=2
first_cell_in_col=".this"
for line in f:
        if count_of_lines>=3:
                first_cell_in_col=str(count_of_lines-2)
        lst = line.split(' ')
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = { "valueInputOption": "USER_ENTERED", "data": [{"range": "List_of_all_inventarizateon!A"+str(count_of_lines)+":C"+str(count_of_lines),"majorDimension": "COLUMNS","values": [[first_cell_in_col],['https://docs.google.com/spreadsheets/d/' + lst[0]] ,[ lst[1] ]]}]}).execute()
        count_of_lines+=1
f.close()
def get_grid_id(service):
    response = service.spreadsheets().get(spreadsheetId=spreadsheetId, includeGridData=True).execute()
    return response['sheets'][0]['properties']['sheetId']
def sheets_update(sheets_service, grid_id):
    body = {"requests": [{"autoResizeDimensions": {"dimensions": {"sheetId": grid_id, "dimension": "COLUMNS" }}}]}
    response = sheets_service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()
sheets_update(service, get_grid_id(service))
