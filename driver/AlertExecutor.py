import sys
from alert import email_alert
from alert import slack_alert
from curlCheck import curlAlert

class AlertExecutor():
    def __init__(self, configData):
        self.configData = configData
        self.alertConfig = configData['alertConfig']
        print("\n print alert config ", self.alertConfig)
        self.alertSetup = configData['alertSetup']
        self.channelObjects = self.setChannelObject(self.alertConfig['channel'])
        self.messageConfig = self.configData['alertConfig']['messageConfig']
        print("message config : ", self.messageConfig)

    def setChannelObject(self, alertChannel):
        alertChannelList = alertChannel.split(",")
        channelList = []
        for channel in alertChannelList:
            if channel.lower() == 'email':
                self.emailObject = email_alert(self.configData['alertConfig']['serverConfigs']['email'])
                channelList.append(self.emailObject)

            elif channel.lower() == 'slack':
                print(self.configData['alertConfig']['serverConfigs']['slack'])
                self.slackObject = slack_alert(self.configData['alertConfig']['serverConfigs']['slack'])
                channelList.append(self.slackObject)

            else:
                print("invalid choice please provide appropriate alert channel ")
                sys.exit()
        return channelList

    def checkStatus(self, alertType):
        if alertType.lower() == "curl":

            curlAlert.checkCurlAlert(self.alertSetup,self.channelObjects,self.messageConfig)
            #CurlAlert.checkCurlAlert(self.alertSetup)
        elif alertType.lower() == "s3":
            pass
        else:
            print("please check alert type in configuration file , not a valid alertype")
            sys.exit()


    #
    # def triggerAlert(self):
    #     for channel in self.channelObjects:
    #         channel.raiseAlert(self.messageConfig)
