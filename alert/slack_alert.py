import datetime
import json
import sys
import traceback
import requests
from slack_sdk import WebClient  # pip3 install slack_sdk
from slack_sdk.errors import SlackApiError


class slack_alert:
    def __init__(self, slack_config):
        self.slack_config = slack_config
        self.slack_channel = slack_config['slackChannel']

    def raiseAlert(self, messageConfig):
        alert_subject = messageConfig['alert_subject']
        alert_priority = messageConfig['alert_priority']
        alert_module = messageConfig['alert_module']
        alert_detail = messageConfig['alert_detail']
        # if alertSetup['type'].lower() == 'curl':
        #     alert_detail = "Ip - " + alertSetup['typeProperties']['hostname'] + " - " + alert_detail
        # else:
        #     pass
        alert_channel = self.slack_channel
        block = """
                    [{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "` Alert`: _{alert_subject}_ | _{alert_priority}_ | _{alert_module}_ | _{alert_detail}_ | _{alert_channel}_ > Alert"
                        }
                    }]"""
        updatedBlock = block.replace("{alert_subject}", alert_subject).replace("{alert_priority}",
                                                                               alert_priority).replace(
            "{alert_module}", alert_module).replace("{alert_detail}", alert_detail).replace("{alert_channel}",
                                                                                            alert_channel)
        slack_block = json.dumps(json.loads(updatedBlock
                                            ))

        if "slackToken" in self.slack_config:
            try:
                slack_token = self.slack_config['slackToken']
                # slack_client
                slack_client = WebClient(
                    token=slack_token)  # Webclient created
                channel = self.slack_channel
                print("Sending Slack alert ....")
                response = slack_client.chat_postMessage(
                    channel=channel,
                    text="This is an Production Alert",
                    blocks=slack_block
                )
                # (200 is OK, 404 is Not Found)
                print("TIMESTAMP : ", datetime.datetime.now())
                print('\033[1m' + alert_subject, alert_priority, alert_module, alert_detail, alert_channel, sep=" | ")

                response_dict = {"status": response.status_code,
                                 "message": "Slack Alert Raised"}
                response = json.dumps(response_dict)
                print("Response is: " + response)
                # returning json obj
                return response

            except SlackApiError as e:
                # You will get a SlackApiError if "ok" is False
                # str like 'invalid_auth', 'channel_not_found'
                assert e.response["error"]
                print("-------------------------------------------------")
                traceback.print_exc()
                print("-------------------------------------------------")
                print(e)


        elif "webhookUrl" in self.slack_config:
            # data = {
            #     'text': slack_block,
            #     'username': 'HAL',
            #     'icon_emoji': ':robot_face:'
            # }
            message = json.loads(slack_block)
            data = {
                'Alert': 'This is production alert',
                "text": message[0]['text']['text']
            }
            webhook_url = self.slack_config['webhookUrl']
            response = requests.post(webhook_url
                                     , data=json.dumps(data)
                                     , headers={'Content-Type': 'application/json'}
                                     )

        else:
            print(
                "Entered Wrong configuration of slack neither slack_token nor webhook !!!!")
            sys.exit()
        print("slack Alert Triggered!")
