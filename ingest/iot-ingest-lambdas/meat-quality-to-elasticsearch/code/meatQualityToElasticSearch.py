import json
import os
import requests
import datetime
import uuid

ELASTIC_SEARCH_URL="https://search-peroxide-cloud-analytic-k6yj2lsthozla5csivsjbdocpu.ap-southeast-2.es.amazonaws.com"
INDEX_TYPE="/iotcsv/iotcsv/"
HEADERS = {'Content-Type':'application/json'}


def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        if record['eventName'] != 'REMOVE':
            rawJson = record['dynamodb']['NewImage']
            data = {
                "item":rawJson['item']['S'],
                "device_id":rawJson['device_id']['S'],   
                "quality_score":rawJson['quality_score']['N'],   
                "created_date":rawJson['created_date']['S'],   
                "id":rawJson['id']['S'],   
                "group":rawJson['group']['S'],   
                "quality_value":rawJson['quality_value']['N'],
                "freq_from":rawJson['freq_from']['N'],
                "freq_sample_num":rawJson['freq_sample_num']['N']
              }
            # url = ELASTIC_SEARCH_URL+INDEX_TYPE+data["device_id"]+'_'+data["iot_created"]
            url = ELASTIC_SEARCH_URL+INDEX_TYPE+data['id']
            print(url)
            print(data) 
            try:
                res = requests.post(
                    url,
                    headers=HEADERS,
                    data=json.dumps(data)
                )
                print(res)
            except Exception as e:
                print('error: ', e)  
        
  

    return {
        'statusCode': 200,
        'body': json.dumps({})
    }
