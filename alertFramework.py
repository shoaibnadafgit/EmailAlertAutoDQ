import argparse
import json
from driver import AlertExecutor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Please Provide required arguments ")
    parser.add_argument("-c", "--config", required=True,
                        help="provide alertProperties.json file path")

    args = vars(parser.parse_args())
    try:
        with open(args['config'])as f:
            configData = json.load(f)
        if configData:
            alertExecutorObject = AlertExecutor(configData)
            alertExecutorObject.checkStatus(configData['alertSetup']['type'])
        else:
            print("No data in config file . Please check your config file!")
    except Exception as e:
        print("Error occurred : ", e)
