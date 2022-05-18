from pprint import pprint
import httplib2
import apiclient.discovery
import sys
import os.path
import googleapiclient.errors
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
current_datetime = datetime.now()
def htmlColorToJSON(htmlColor):
    if htmlColor.startswith("#"):
        htmlColor = htmlColor[1:]
    return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0, "blue": int(htmlColor[4:6], 16) / 255.0}
class SpreadsheetError(Exception):
    pass
class SheetNotSetError(SpreadsheetError):
    pass
if os.path.exists('.proect_all_spreadsheet'):
        title_spreadsheet='DIP_Invenе_№ '+str((sum(1 for line in open('.proect_all_spreadsheet', 'r'))))
        title_sheet='List_of_all_inventarizateon'
        rowCount=30
        columnCount=1000
else:
    title_spreadsheet='DIP_Main_sheet'
    title_sheet='List_of_all_inventarizateon'
    rowCount=1000
    columnCount=3
CREDENTIALS_FILE = 'diplosheets-4490f33dbc26.json' 
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) 
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) 
spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': title_spreadsheet, 'locale': 'en_US', 'timeZone': 'Etc/GMT'},
    'sheets': [{'properties': {'sheetType': 'GRID', 'sheetId': 0, 'title': title_sheet, 'gridProperties': {'rowCount': rowCount, 'columnCount': columnCount}}}] }).execute()
spreadsheetId = spreadsheet['spreadsheetId']
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'yura1veremij@gmail.com'}, fields = 'id' ).execute()
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
shareRes = driveService.permissions().create( fileId = spreadsheet['spreadsheetId'],
    body = {'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
    fields = 'id' ).execute()
f = open('.proect_all_spreadsheet', 'a')
f.write(str(spreadsheetId) + " " + current_datetime.isoformat()+"\n")
f.close()
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId+"\n")
