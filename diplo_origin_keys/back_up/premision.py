from pprint import pprint
import httplib2
import apiclient.discovery
import googleapiclient.errors
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'diplosheets-4490f33dbc26.json'  # Имя файла с закрытым ключом, вы должны подставить свое
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheetId = "1or7MiiIZPnV4eUiHt5JwAX_mbApCtxI5qD2RbH72Sqs"

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
shareRes = driveService.permissions().create(
    fileId = spreadsheet['spreadsheetId'],
    body = {'type': 'anyone', 'role': 'reader'},  # доступ на чтение кому угодно
    fields = 'id'
).execute()

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 'yura1veremij@gmail.com'},  # Открываем доступ на редактирование
    fields = 'id'
).execute()
