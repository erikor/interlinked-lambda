import os
import datetime
import json
from gzip import GzipFile
from io import BytesIO
try:
    import boto3

except ImportError:
    sys.path.append('lib')
    import boto3

def check_exists(key, bucket, subdir):
    subdir = format_dir(subdir)
    s3 = boto3.client('s3')
    status = 200
    status_body = {'result': 'ok'}
    try:
        res = s3.head_object(
            Bucket = bucket,
            Key = subdir + key
        )
        debug(key + " !!!!!!!! EXISTS: " + str(res))
    except Exception as e:
        status = 404
        status_body = {'result': 'object ' + subdir + key + 'does not exist',
                       'message': str(e)}

    return {'statusCode': status,
        'body': status_body,
        'headers': {'Content-Type': 'application/json'}}

def store_item(key, data, bucket, subdir, gzip = False):
    encode = "none"
    subdir = format_dir(subdir)
    if gzip:
        data = zipit(data)
        encode = "gzip"

    s3 = boto3.client('s3')
    status = 200
    status_body = {'result': 'ok'}
    try:
        s3.put_object(
            Bucket = bucket,
            Key = subdir + key,
            ContentType = 'application/json', 
            ContentEncoding = encode,
            Body = data
        )
    except Exception as e:
        status_body = str(e)
        status = 501

    return {'statusCode': status,
        'body': json.dumps(status_body),
        'headers': {'Content-Type': 'application/json'}}

def get_item(key, bucket, subdir, gzip = False):
    subdir = format_dir(subdir)
    s3 = boto3.client('s3')
    obj = s3.get_object(
            Bucket = bucket,
            Key = subdir + key
          )
          
    if (gzip):
        data = unzipit(obj['Body'])
    else:
        data = obj['Body'].read().decode('utf-8') 
        
    return {'statusCode': 200,
        'body': data,
        'headers': {'Content-Type': 'application/json'}}
 
# Kudos to @veselosky on GitHub for help with the compression
def unzipit(s):
    bytestream = BytesIO(s.read())
    data = GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8')
    return data

def zipit(s):
    gz_body = BytesIO()
    gz = GzipFile(None, 'wb', 9, gz_body)
    gz.write(s.encode('utf-8')) 
    gz.close()
    return gz_body.getvalue()

def format_dir(s):
    s = os.path.join(s, "")
    s = s.replace("\\", "/") # os independent
    return s

def debug(s):
    bucket = "interlinked"
    subdir = "log"
    key = "DEBUG"
    try:
        log = interlinked.get_item(key, bucket, subdir, False)
        body = log['body']
    except Exception as e:
        body = ""

    body = str(datetime.datetime.now()) + " " + s + "\n" + body 

    # only preserve the last 5000 logs
    body = "\n".join(body.split('\n')[0:4999])

    return(store_item(key, body, bucket, "log", False))