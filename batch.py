import sys
import os
import uuid
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json
import datetime
from lib import interlinked
import pdb

# Kudos to @veselosky on GitHub for help with the compression
def submit(event, context):
    payload = json.loads(event['body'])
    bucket = "interlinked"
    subdir = "jobs"

    if "debug" not in payload:
        debug = False
    else:
        debug = payload['debug']

    key = str(uuid.uuid4())
    function = payload['function']
    name = payload['name']
    script = payload['script']
    arguments = payload['arguments']
    job = {
        "script": script,
        "function": function,
        "name": name,
        "arguments": arguments
    }
    if debug:
        interlinked.debug("Saving job to S3: " + json.dumps(job))
    res = interlinked.store_item(key, json.dumps(job), bucket, subdir, False)
    if debug:
        interlinked.debug("Job " + key + " sent to S3. Result: " + json.dumps(res)

    )
    return {'statusCode': 200,
            'body': json.dumps(res),
            'headers': {'Content-Type': 'application/json'}}
