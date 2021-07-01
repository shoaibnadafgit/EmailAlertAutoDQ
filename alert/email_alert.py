import glob
import datetime
import json
import os
import re
import traceback
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP


class email_alert:
    def __init__(self, email_config):
        self.email_config = email_config

    def send_emailReport(self, messageConfig):
        # report sending code --------
        global server
        
        try:
            port = self.email_config['smtp_port']
            smtp_server = self.email_config['smtp_server']
            sender_email = self.email_config['user']
            receiver_email = self.email_config['recipient']
            
            #alert_subject = messageConfig['alert_subject']
            #alert_priority = messageConfig['alert_priority']
            #alert_module = messageConfig['alert_module']
            #alert_detail = messageConfig['alert_detail']
            report_Sub = messageConfig['Subject'] 
            #att_dir = messageConfig['dir']
            list_attach = messageConfig['attach'] 
            detail = messageConfig['Body']
            
            # SMTP Object creation
            server = SMTP(smtp_server, port)
            # email validation regex
            checker = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

            if (re.search(checker, sender_email)):
                password = self.email_config['password']
                message = MIMEMultipart("alternative")
                message["Subject"] = report_Sub#+" | "+alert_subject +" | "+ alert_priority +" | "+ alert_module +" | "+ alert_detail
                message["From"] = sender_email
                message["To"] = receiver_email
                text = detail
                message.attach(MIMEText(text, 'plain'))


                
                
                pdf_dir = list_attach

                pdf_files = glob.glob("%s/*.pdf" % pdf_dir)
                for f in pdf_files:
                    # less than 35 MB ~ 35000000 bytes
                    if os.path.getsize(f) < 35000000:
                        # Open the file as binary mode
                        attach_file = open(f, 'rb')
                        payload = MIMEBase('application', 'octate-stream')
                        payload.set_payload((attach_file).read())
                        # encode the attachment
                        encoders.encode_base64(payload)
                        filename =f.split("/")
                        n = len(filename)-1
                        print(filename[n])
                        # add payload header with filename
                        payload.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {filename[n]}",  
                        )
                        message.attach(payload)

                    else:
                        print("Size of attachments exceeds limit 35MB !!!")
                        break
                server.starttls()  # encrypt it using .starttls().
                server.login(sender_email, password)
                print("Sending Report .....")
                # by this we can send multiple emails separated by ','
                response = server.sendmail(sender_email, receiver_email.split(','), message.as_string())
                # server.sendmail(sender_email, receiver_email, message)
                print("Report sent successfully !!!")
                print("TIMESTAMP : ", datetime.datetime.now())
                print('\033[1m' + report_Sub, list_attach, detail, sep=" | ")
                status = server.noop()
                response_dict = {
                    "status": status[0 - 2], "massage": "Email Alert Raised"}
                response = json.dumps(response_dict)
                print("Response is: " + response)
                return response  # returning json obj
            else:
                raise Exception(
                    "Entered Wrong email id as per email format !!!")
        except Exception as e:
            traceback.print_exc()
        finally:
            print("Server connection closed")
            server.quit()

    def raiseAlert(self, messageConfig):
        alert_subject = messageConfig['alert_subject']
        alert_priority = messageConfig['alert_priority']
        alert_module = messageConfig['alert_module']
        alert_detail = messageConfig['alert_detail']
        sender_email = self.email_config['sender_email']
        # if alertSetup['type'].lower() == 'curl':
        #     alert_detail = "Ip : " + alertSetup['typeProperties']['hostname'] + " - " + alert_detail
        user = self.email_config['user']
        print("raise alert email ")
        port = self.email_config['smtp_port']
        smtp_server = self.email_config['smtp_server']
        receiver_email = self.email_config['recipient']
        # email validation regex
        checker = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        # email sending code --------
        try:
            # SMTP Object creation
            server = SMTP(smtp_server, port)
            if (re.search(checker, sender_email)):
                password = self.email_config['password']
                message = MIMEMultipart("alternative")
                message["Subject"] = alert_subject + " | " + alert_priority + \
                                     " | " + alert_module
                message["From"] = sender_email
                message["To"] = receiver_email
                html = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>.alert {padding: 20px;background-color: #f44336;color: white;}.closebtn {" \
                       "margin-left: 15px;color: white;font-weight: bold;float: right;font-size: 22px;line-height: " \
                       "20px;cursor: pointer;transition: 0.3s;}.closebtn:hover {color: " \
                       "black;}</style></head><body><h2 style=""color:red;font-size:24px;"f">{alert_subject}  Alert Message</h2><p style=""color:black;font-size:18px;"f" > {alert_detail} .</p><div style=""color:black;font-size:16px;""" \
                       "class='email_alert'><span class='closebtn'>&times;</span> <strong style=""color:black;font-size:18px;"">Error!</strong>Please Check.</div></body></html>"

                part = MIMEText(html, "html")
                message.attach(part)
                server.starttls()  # encrypt it using .starttls().
                server.login(user, password)
                print("Sending email .....")
                # by this we can send multiple emails seperated by ','
                response = server.sendmail(sender_email, receiver_email.split(','), message.as_string())
                print("Email sent successfully !!!")
                print("TIMESTAMP : ", datetime.datetime.now())
                print('\033[1m' + alert_subject, alert_priority, alert_module, alert_detail, sep=" | ")
                # (250 is OK)
                status = server.noop()
                response_dict = {
                    "status": status[0 - 2], "massage": "Email Alert Raised"}
                response = json.dumps(response_dict)
                print("Response is: " + response)
                return response  # returning json obj
            else:
                raise Exception(
                    "Entered Wrong email id as per email format !!!")

        except Exception as e:
            traceback.print_exc()
        finally:
            print("Server connection closed")
            server.quit()
