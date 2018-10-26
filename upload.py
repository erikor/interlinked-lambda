import sys
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json
import datetime

def handler(event, context):
    return {'statusCode': 200,
            'body': json.dumps(event),
            'headers': {'Content-Type': 'application/json'}}
            
