

def triggerAlert(channelObjects,messageConfig):
    for channel in channelObjects:
        channel.raiseAlert(messageConfig)