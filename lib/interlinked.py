import os
from gzip import GzipFile
from io import BytesIO
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3

def store_item(key, data, bucket, subdir, gzip = False):
    encode = "none"
    subdir = format_dir(subdir)
    if gzip:
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
