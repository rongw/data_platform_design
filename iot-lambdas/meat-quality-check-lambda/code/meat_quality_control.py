import json
import os
import requests
import datetime
import uuid

# cd package
# zip -r9 ../function.zip .
# cd ..
# zip -rv function.zip meat_quality_control.py
# aws lambda update-function-code --function-name meatQualityControl --zip-file fileb://function.zip

import json
import os
import requests
import datetime
import uuid

def lambda_handler(event, context):
    print(event)
    rawJson = event
    Z = float(os.environ['CONSTANT_ADJUST_VALUE'])
    value = 0;

    for dia in rawJson["dia"]:
        r = dia["r"]
        i = dia["i"]
        value += (Z*2*i)/(((1-r)*(1-r)) + (i*i))
    pass

    avgDia = value/len(rawJson["dia"])


    WATER_DIA = float(os.environ['CONSTANT_WATER_DIA'])
    AIR_DIA = float(os.environ['CONSTANT_AIR_DIA'])

    qualityScore = abs((avgDia - AIR_DIA) / (WATER_DIA - AIR_DIA))
    qualityScore = (qualityScore * qualityScore * qualityScore) * 100;

    post_body = {
        "query" : "mutation createFoodquality($createfoodqualityinput: CreateFoodqualityInput!) {createFoodquality(input: $createfoodqualityinput) {id group device_id quality_value item}}",
        "operationName" : "createFoodquality",
        "variables": {
            "createfoodqualityinput" : {
                "group" : rawJson["iot_group"],
                "device_id" : rawJson["iot_dev_id"],
                "quality_value" : avgDia,
                "quality_score" : qualityScore,
                "item" : rawJson["iot_type"],
                "created_date" : rawJson["iot_created"],
                "freq_from" : rawJson["freq_from"],
                "freq_to" : rawJson["freq_to"],
                "freq_sample_num" : rawJson["freq_sample_num"]
            }
        }
    }

    graphQlApi = os.environ['GRAPHQL_API_URL']
    graphQlApiKey = os.environ['GRAPHQL_API_KEY']

    try:
        res = requests.post(
            graphQlApi,
            headers={"x-api-key" : graphQlApiKey, "Content-Type": "application/graphql"},
            data=json.dumps(post_body)
        )
    except Exception as e:
        print('error: ', e)

    return {
        'statusCode': 200,
        'body': json.dumps(avgDia)
    }
