# Подключаем библиотеки
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import os.path
from pathlib import Path
CREDENTIALS_FILE = 'diplosheets-4490f33dbc26.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе

service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API

spreadsheetId = "1or7MiiIZPnV4eUiHt5JwAX_mbApCtxI5qD2RbH72Sqs"

results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
	"data": [
        {"range": "List_of_PC!A1:A13",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values": [
                    ["TIME"],
                    ["IP_addres"], # Заполняем первую строку
                    ["OS_bild_kernel"],
                    ["Procesor"],
                    ["Grafic_card"],
                    ["Amount_of_RAM"],
                    ["RAM_description"],
                    ["Hard_drive"],
                    ["BIOS"],
                    ["Mpther_board"],
                    ["Network_card"],
                    [""],
                    ["INFO_from_\"LSHW\""]
                   ]}
    ]
}).execute()


count = 1
while os.path.isfile("temp"+str(count)):
	file = open("temp"+str(count), "r")
	i=0
	for line in file:
		i+=1
		results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
			"valueInputOption": "USER_ENTERED",
			"data": [
			{"range": "List_of_PC!"+chr(65+count)+str(i)+":"+chr(65+count)+str(i),
			"majorDimension": "ROWS",  
			"values": [
			[line]]}]
			}).execute()
	count+=1


file.close()
count = 1

while os.path.isfile("all"+str(count)+".txt"):
	file = open("all"+str(count)+".txt", "r")
	lshw = file.read()
	results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
                "valueInputOption": "USER_ENTERED",
                "data": [
       	        {"range": "List_of_PC!"+chr(65+count)+"13:"+chr(65+count)+"13",
                "majorDimension": "ROWS",
                "values": [
                [lshw]]}]
                }).execute()
	count+=1
file.close()
