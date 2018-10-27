import sys
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json
import datetime

def handler(event, context):
    #data = [19, "A", 43, "B"]
    #s3 = boto3.resource('s3')
    #obj = s3.Object('interlinked','test/hello.tab')
    #obj.put(Body='\n'.join(str(e) for e in data))
    #obj = s3.Object('interlinked','test/hello.tab')
    #data = obj.get()['Body'].read().decode('utf-8') 

    #obj.put(Body='\n'.join(str(e) for e in data))
    payload = json.loads(event['body'])
    key = payload['key']
    data = payload['data']
    return {'statusCode': 200,
            'body': "\n".join(str(s) for s in data),
            'headers': {'Content-Type': 'application/json'}}
            
