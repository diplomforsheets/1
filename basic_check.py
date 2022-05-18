import smtplib
from email.mime.text import MIMEText
import os.path
from pathlib import Path
import os
import re
import filecmp
class Gmail(object):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.server = 'smtp.gmail.com'
        self.port = 587
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo
        session.login(self.email, self.password)
        self.session = session
    def send_message(self, subject, body):
        ''' This must be removed '''
        headers = [
            "From: " + self.email,
            "Subject: " + subject,
            "To: " + self.email,
            "MIME-Version: 1.0",
           "Content-Type: text/html"]
        headers = "\r\n".join(headers)
        self.session.sendmail(
            self.email,
            self.email,
            headers + "\r\n\r\n" + body)
count = 1
while os.path.exists("temp"+str(count)):
        var=1
        while os.path.isfile("temp"+str(count)+"/"+str(var)):
                f1="temp"+str(count)+"/"+str(var)
                f2="temp.check"+str(count)+"/"+str(var)
                if not filecmp.cmp(f1, f2, shallow=False):
                        print("Warning !!! change in last oblick in List_of_all_inventarizateon!"+chr(65+count)+str(var)+":"+chr(65+count)+str(var))
                        gm = Gmail('2020.diplom.forsheets@gmail.com', 'smtp.gmail.com')
                        gm.send_message('Warning!!!', "change in List_of_all_inventarizateon!"+chr(65+count)+str(var)+":"+chr(65+count)+str(var))
                var+=1
        count+=1
      
