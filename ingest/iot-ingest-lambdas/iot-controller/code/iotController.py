import boto3
import json
import requests
import datetime
import simplejson

# json.JSONEncoder.default = lambda self,obj: (
#         obj.isoformat() if isinstance(obj, datetime.datetime) 
#         else None
#     )

def request_handler(event, context):
    print(event)

    iotClient = boto3.client('iot')
    iotDatclient = boto3.client('iot-data')
    cloudwatchClient = boto3.client('cloudwatch')

    # resp = iotClient.list_things()

    # resp = cloudwatchClient.list_metrics()
    # print(resp)
    resp = {
            "isBase64Encoded": "false",
            "statusCode": 200,
            "headers": { "Content-Type": "application/json"},
            "body": "{}"
        }

    # if event['pathParameters']['proxy'] == 'metrics':
    #         itemData = {
    #                 "FileId":fileId,
    #                 "Device": device,
    #                 "Collected":collected,
    #                 "Data":json.dumps(jsonData["vs"])
            
    #                }
    #         addResponse = table.put_item(
    #                     Item=itemData
    #                 )
    


    return resp        
