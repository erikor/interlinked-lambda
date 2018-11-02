import sys
from lib import interlinked
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json
import datetime
from gzip import GzipFile
from io import BytesIO

#python -m unittest discover tests
def store(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    if "subdir" not in payload:
        subdir = ""
    else:
        subdir = payload['subdir']

    key = payload['key']
    data = payload['data']
    data = json.dumps(data)
    
    if("gzip" in payload):
        gzip = payload['gzip']
    else:
        gzip = False
        
    return(interlinked.store_item(key, data, bucket, subdir, gzip))
        
def bulk(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    
    if "gzip" in payload:
        gzip = payload['gzip']
    else:
        gzip = False

    if "subdir" not in payload:
        subdir = ""
    else:
        subdir = payload['subdir']
        
    keys = payload['keys']
    data = payload['data']
    for i in range(len(keys)):
        interlinked.store_item(keys[i], json.dumps(data[i]), bucket, subdir, gzip)
    return {'statusCode': 200,
        'body': "ok",
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

