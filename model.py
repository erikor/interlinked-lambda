import sys
import os
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json
import datetime
from gzip import GzipFile
from io import BytesIO


# Kudos to @veselosky on GitHub for help with the compression

def store(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    if("subdir" in payload):
        subdir = os.path.join(payload['subdir'], "")
    else:
        subdir = ""
    key = payload['key']
    data = payload['data']
    data = json.dumps(data)
    
    if("gzip" in payload):
        gzip = payload['gzip']
    else:
        gzip = False
        
    return(load_item(key, data, bucket, subdir, gzip))

    
        
def bulk(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    
    if("gzip" in payload):
        gzip = payload['gzip']
    else:
        gzip = False

    if("subdir" in payload):
        subdir = os.path.join(payload['subdir'], "")
    else:
        subdir = ""
        
    keys = payload['keys']
    data = payload['data']
    for i in range(len(keys)):
        load_item(keys[i], json.dumps(data[i]), bucket, subdir, gzip)
    return {'statusCode': 200,
        'body': "ok",
        'headers': {'Content-Type': 'application/json'}}
        
        
def load_item(key, data, bucket, subdir, gzip = False):
    encode = "none"
    if(gzip):
        data = zipit(data)
        encode = "gzip"

    s3 = boto3.client('s3')
    s3.put_object(
        Bucket = bucket,
        Key = subdir + key,
        ContentType = 'application/json', 
        ContentEncoding = encode,
        Body = data
    )
    return {'statusCode': 200,
        'body': "ok",
        'headers': {'Content-Type': 'application/json'}}



def fetch(event, context):
    payload = json.loads(event['body'])
    bucket = payload['bucket']
    if("subdir" in payload):
        subdir = os.path.join(payload['subdir'], "")
    else:
        subdir = ""
        
    if("gzip" in payload):
        gzip = payload['gzip']
    else:
        gzip = False
        
    key = payload['key']
    s3 = boto3.client('s3')
    obj = s3.get_object(
            Bucket = bucket,
            Key = subdir + key
          )
          
    if (gzip):
        bytestream = BytesIO(obj['Body'].read())
        data = GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8')
    else:
        data = obj['Body'].read().decode('utf-8') 
        
    return {'statusCode': 200,
        'body': data,
        'headers': {'Content-Type': 'application/json'}}

def zipit(s):
    gz_body = BytesIO()
    gz = GzipFile(None, 'wb', 9, gz_body)
    gz.write(s.encode('utf-8')) 
    gz.close()
    return gz_body.getvalue()
