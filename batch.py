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
    function = payload['func']
    name = payload['name']
    script = payload['script']
    arguments = payload['arguments']
    job_d = {
        "script": script,
        "func": function,
        "name": name,
        "arguments": arguments
    }
    if debug:
        interlinked.debug("Saving job to S3: " + json.dumps(job_d))
    res = interlinked.store_item(key, json.dumps(job_d), bucket, subdir, False)
    if debug:
        interlinked.debug("Job " + key + " sent to S3. Result: " + json.dumps(res)

    )
    client = boto3.client('batch', region_name = 'ca-central-1')
    job = client.submit_job(jobName='interlinked_lambda_job',
                            jobQueue='interlinked',
                            jobDefinition='smalljob:1',
                            containerOverrides={
                                'environment': [
                                    {
                                        'name': 'LAMBDA_JOB_ID',
                                        'value': key
                                    }]
                                }
                            )

    return {'statusCode': 200,
            'body': json.dumps(job),
            'headers': {'Content-Type': 'application/json'}}
