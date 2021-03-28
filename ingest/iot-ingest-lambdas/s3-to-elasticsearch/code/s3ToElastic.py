import boto3
import json
import requests
import datetime

ELASTIC_SEARCH_URL="https://search-peroxide-cloud-iot-fjfkb5nwyv3crkxb2orx7cfdu4.ap-southeast-2.es.amazonaws.com"
INDEX_TYPE="/iotcsv/iotcsv/"
HEADERS = {'Content-Type':'application/json'}

ORG_BUCKET = "iot-signal-csv"
PROCESS_BUCKET = "iot-signal-csv-processed"
FAILED_BUCKET = "iot-signal-csv-failed"

def request_handler(event, context):
    print(event)
    s3 = boto3.resource('s3')

    fileName = event['Records'][0]['s3']['object']['key']

    originCsvBucket = s3.Bucket(ORG_BUCKET)
    processBucket = s3.Bucket(PROCESS_BUCKET)
    failedBucket = s3.Bucket(FAILED_BUCKET)

    prefix = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    recordCount = 0

    # for object in originCsvBucket.objects.all():
    # fileName = object.key
    fileId = fileName[0:fileName.index('_')]
        
        
    obj = s3.Object(bucket_name=ORG_BUCKET, key=fileName)
    response = obj.get()
    jsonData = json.loads(response['Body'].read().decode("utf-8")) 

    device = jsonData["device"]
    collected = jsonData["collected"]
    for row in jsonData['vs']:
            url = ELASTIC_SEARCH_URL+INDEX_TYPE+fileId+'_'+str(recordCount)
            print(url)
            row['device'] = device
            row['collected'] = collected  
            row['fileId']=fileId      
            response = requests.post(url,headers=HEADERS,data=json.dumps(row))
            print(response)        
            recordCount = recordCount + 1
        
    copy_source = {
                'Bucket':ORG_BUCKET,
                'Key':fileName
            }
    processBucket.copy(copy_source,fileName)
    delResp = originCsvBucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': fileName
                        
                    },
                ],
                'Quiet': True
            }
            
    )

    data={
        "processed_records":recordCount,
        "processed_file":fileName
    }

    resp = {
            "isBase64Encoded": "false",
            "statusCode": 200,
            "headers": { "Content-Type": "application/json"},
            "body": json.dumps(data)
    	    }
    print(resp)            
    return resp 

