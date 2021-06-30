import fpdf
from fpdf import FPDF 
from create_table_fpdf2 import PDF

class NotificationSender:
    def __init__(self,notification_id):
        self.notification_id = notification_id

    def display(self):
        print("ds 0",self.notification_id[0:1])
       

    def storePDF(self):
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Times", size=10)
        data = self.notification_id[0:2]
        tabledata = self.notification_id[2:]
        pdf.create_table(table_data = data,title='Data Source "ds1" ', cell_width='even') 
        pdf.ln()
        pdf.create_table(table_data = tabledata,title='Details of table from Data Source "ds1" ', cell_width='even') 
        pdf.ln()
        

        pdf.output('table_class.pdf')


#-------------------------------------------------------------------------------------------------#

def getNotification_id():
    data = [
        ["Data source", "Type", "Catalog compilation %", "past 7 days Improvements","pas 30 days Improvements","Total object count","Tracked object","Owner",], # 'testing','size'],
        ["ds1", "mysql", "34", "-4","20","223","120","ajitr",], # 'testing','size'],
        ["Data source", "Object schema","Object name", "Catalog compilation %", "past 7 days Improvements","pas 30 days Improvements","Owner","Jira",], # 'testing','size'],
        ["ds1", "schema1","table1","34","-4","20","ajitr","https://jira",], # 'testing','size'],
        ["ds1", "schema1","table2","34","-4","2","ajitr","https://jira",], # 'testing','size'],

    ]
    return data 

notification_id = getNotification_id()
n1 = NotificationSender(notification_id)
n1.display()
n1.storePDF()

