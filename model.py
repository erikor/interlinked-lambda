import sys
import datetime
from lib import interlinked
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json
from time import sleep
from gzip import GzipFile
from io import BytesIO

def mdebug(s):
    e = {"body": json.dumps({
        "bucket": "interlinked",
        "level": "MDEBUG",
        "message": s
    })}
    log(e, None)
    
def check(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    if "subdir" not in payload:
        subdir = ""
    else:
        subdir = payload['subdir']

    key = payload['key']        
    return(interlinked.check_exists(key, bucket, subdir))

def store(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']

    if "subdir" not in payload:
        subdir = ""
    else:
        subdir = payload['subdir']

    if "overwrite" in payload:
        overwrite = payload['overwrite']
    else:
        overwrite = True

    key = payload['key']
    data = payload['data']
    data = json.dumps(data)

    res = interlinked.check_exists(key, bucket, subdir)
    if res['statusCode'] == 200 and not overwrite:
        return {'statusCode': 202,
            'body': {'message': 'items exists and not overwritten'},
            'headers': {'Content-Type': 'application/json'}}
    else: 
        if("gzip" in payload):
            gzip = payload['gzip']
        else:
            gzip = False    

        return(interlinked.store_item(key, data, bucket, subdir, gzip))
        
def bulk(event, context):
    success_count = 0
    pre_existing = 0
    status = 200
    message = 'ok'
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    
    if "gzip" in payload:
        gzip = payload['gzip']
    else:
        gzip = False

    if "overwrite" in payload:
        overwrite = payload['overwrite']
    else:
        overwrite = True

    if "subdir" not in payload:
        subdir = ""
    else:
        subdir = payload['subdir']
        
    keys = payload['keys']
    data = payload['data']
    for i in range(len(keys)):
        if overwrite:
            res = interlinked.store_item(keys[i], json.dumps(data[i]), bucket, subdir, gzip)
            if res['statusCode'] == 200:
                success_count += 1
            else:
                status = 202
                message = "LAST ERROR: " + res['body']
        else:
            res = interlinked.check_exists(keys[i], bucket, subdir)
            if res['statusCode'] == 200:
                pre_existing += 1
            elif res['statusCode'] == 404:
                mdebug("storing: " + keys[i])
                res = interlinked.store_item(keys[i], json.dumps(data[i]), bucket, subdir, gzip)
                if res['statusCode'] == 200:
                    mdebug("stored: " + keys[i])
                    success_count += 1
                else:
                    status = 202
                    message = "LAST ERROR: " + res['body']
            else:
                status = 500
                message = "Unhandled error on check_exists: " + res['body']
                return {'statusCode': status,
                    'body': json.dumps({'objects_sent': len(keys), 
                            'objects_saved': success_count,
                            'pre_existing_objects': pre_existing,
                            'message': message}),
                    'headers': {'Content-Type': 'application/json'}}
            
    return {'statusCode': status,
        'body': json.dumps({'objects_sent': len(keys), 
                 'objects_saved': success_count,
                 'pre_existing_objects': pre_existing,
                 'message': message}),
        'headers': {'Content-Type': 'application/json'}}
        
def fetch(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    if "subdir" not in payload:
        subdir = ""
    else:
        subdir = payload['subdir']

    if("gzip" in payload):
        gzip = payload['gzip']
    else:
        gzip = False
        
    key = payload['key']
    return interlinked.get_item(key, bucket, subdir, gzip)

def log(event, context):
    payload = json.loads(event['body'])
    print("LOG EVENT: " + payload['level'] + " " + payload['message'])
    return {'statusCode': 200,
            'body': {'result': 'ok'},
            'headers': {'Content-Type': 'application/json'}}


