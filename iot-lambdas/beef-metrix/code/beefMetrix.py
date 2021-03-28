import boto3
import json
import uuid
import datetime
from boto3.dynamodb.conditions import Key, Attr

table_name = "BeefMetrixTable"

client = boto3.resource('dynamodb')



def request_handler(event, context):
    print(event)
    
    method = event['httpMethod']

    table = client.Table(table_name)

    target = event['pathParameters']['proxy']

    # queryParam = event['queryStringParameters']               
    # print("Received PathParameter:{0}".format(target))
    # print("Received QueryParameter:{0}".format(queryParam))

    # response = "";
    responseBody = []

    if method == 'POST' and target == 'metrix':
        response = table.scan(               
                    Select='COUNT'     
                )
        addCount = response['Count']
        if addCount == 0:
            addCount = 1
        else:
            addCount = addCount + 1        

        requestJson = json.loads(event['body'])
        requestJson['id'] = str(uuid.uuid4())
        strDistribution = [str(i) for i in requestJson['distribution']]

        

        requestData = {
            'Type':requestJson['type'],
            'id':requestJson['id'],
            'Distribution':strDistribution,
            'Description':requestJson['description'],
            'AddCount':addCount
        }
        addResponse = table.put_item(
                Item=requestData
            )
        print(addResponse)

    if method == 'GET' and target == 'metrix':        
        inType = event['queryStringParameters']["type"]  
        countResponse = table.scan(               
                FilterExpression=Attr('Type').eq(inType),
                ProjectionExpression='AddCount'
            )
        print(countResponse)
        addCountList = []
        for item in countResponse['Items']:
            addCountList.append(item['AddCount'])
        
        addCount = max(addCountList)
        print(addCount)

        response = table.scan(               
                FilterExpression=Attr('AddCount').eq(addCount),
                
            )

        responseBody = []
    
        for item in response['Items']:
            data = {}    
            data['type'] = item['Type']
            data['description'] = item['Description']
            data['id'] = item['id']
            distributionList = [float(disbItem) for disbItem in item['Distribution']]                
            data['distribution'] = distributionList
            responseBody.append(data)

    resp = {
            "isBase64Encoded": "false",
            "statusCode": 200,
            "headers": { 
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",            
                "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,PATCH,POST,PUT,DELETE"
                },
            "body": json.dumps(responseBody)
            }

    return resp 


