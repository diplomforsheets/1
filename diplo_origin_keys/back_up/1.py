from pprint import pprint
import httplib2
import apiclient.discovery
import googleapiclient.errors
from oauth2client.service_account import ServiceAccountCredentials

def htmlColorToJSON(htmlColor):
    if htmlColor.startswith("#"):
        htmlColor = htmlColor[1:]
    return {"red": int(htmlColor[0:2], 16) / 255.0, "green": int(htmlColor[2:4], 16) / 255.0, "blue": int(htmlColor[4:6], 16) / 255.0}

class SpreadsheetError(Exception):
    pass

class SpreadsheetNotSetError(SpreadsheetError):
    pass

class SheetNotSetError(SpreadsheetError):
    pass


CREDENTIALS_FILE = 'diplosheets-4490f33dbc26.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе

service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheet = service.spreadsheets().create(body = {
    'properties': {'title': 'Veremij_Inventarization_Diplom', 'locale': 'en_US', 'timeZone': 'Etc/GMT'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'List_of_PC',
                               'gridProperties': {'rowCount': 1000, 'columnCount': 15}}}]
}).execute()




spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'yura1veremij@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()

print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
