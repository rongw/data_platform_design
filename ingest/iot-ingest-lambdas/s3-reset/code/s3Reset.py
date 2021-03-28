import boto3
import json
import requests
import datetime

ELASTIC_SEARCH_URL="https://search-peroxide-cloud-iot-fjfkb5nwyv3crkxb2orx7cfdu4.ap-southeast-2.es.amazonaws.com"
HEADERS = {'Content-Type':'application/json'}

ORG_BUCKET = "iot-signal-csv"
PROCESS_BUCKET = "iot-signal-csv-processed"

def request_handler(event, context):

    s3 = boto3.resource('s3')

    originCsvBucket = s3.Bucket(ORG_BUCKET)
    processBucket = s3.Bucket(PROCESS_BUCKET)

    for object in processBucket.objects.all():
        fileName = object.key
        print(fileName)
        copy_source = {
            'Bucket':PROCESS_BUCKET,
            'Key':fileName
        }
        index = fileName.index('/')+1
        name = fileName[index:]
        print(name)
        originCsvBucket.copy(copy_source,name)
        
    return "DONE"

