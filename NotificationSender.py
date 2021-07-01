import fpdf
from fpdf import FPDF 
from create_table_fpdf2 import PDF
from alert import email_alert
from alert import slack_alert
import json 


class NotificationSender:
    def __init__(self,notification_id):
        self.notification_id = notification_id

    def display(self):
        print("testing...")
       

    def storePDF(self):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Times", size=10)
        untrackeddata = self.notification_id[0:2]    
        data = self.notification_id[2:4]
        tabledata = self.notification_id[4:]
        title = "Data Source "+ self.notification_id[3][0]
        detailtable = 'Details of table from Data Source '+ self.notification_id[3][0]
        pdf.create_table(table_data = untrackeddata,title=title, cell_width='even') 
        pdf.ln()
        
        pdf.create_table(table_data = data,title=title, cell_width='even') 
        pdf.ln()
        pdf.create_table(table_data = tabledata,title=detailtable, cell_width='even') 
        pdf.ln()

        pdf.output('table_class.pdf')

    def sendNotification(self):
        print("sendNotification...")
        configFile  = "/home/shoaib/Dataeaze_Official/AutoDQ_Task/AutoDQ_NotificationHandler/properties/curlAlertProperties.json"
        with open(configFile) as f:
            configData = json.load(f)
            emailConfig = configData["email"]
            slackConfig = configData["slack"]
            print(emailConfig)
            print(slackConfig)
            report_obj = email_alert(emailConfig)

            messageConfig = configData["messageConfig"]
            report_obj.send_emailReport(messageConfig)
#-------------------------------------------------------------------------------------------------#

def getNotification_id():
    data = [
        ["<descreption>","", "<schema name>","","<last sync>","","<untracked obj>","","","",], # 'testing','size'], 0
        ["Data from mysql","", "mysqlschema","","21-06-2021","","435","","","",], # 'testing','size'], 1
        ["Data source", "Type", "Catalog compilation %", "past 7 days Improvements","pas 30 days Improvements","Total object count","Tracked object","Owner",], # 'testing','size'],
        ["ds1", "mysql", "34", "-4","20","223","120","ajitr",], # 'testing','size'], 3
        ["Data source", "Object schema","Object name", "Catalog compilation %", "past 7 days Improvements","pas 30 days Improvements","Owner","Jira",], # 'testing','size'],
        ["ds1", "schema1","table1","34","-4","20","ajitr","https://jira",], # 'testing','size'], 5
        ["ds1", "schema1","table2","34","-4","2","ajitr","https://jira",], # 'testing','size'], 6
    ]
    return data 

notification_id = getNotification_id()
n1 = NotificationSender(notification_id)
n1.display()
n1.storePDF()
n1.sendNotification()



