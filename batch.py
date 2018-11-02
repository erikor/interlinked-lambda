import sys
import os
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
    #pdb.set_trace()
    payload = json.loads(event['body'])
    bucket = "interlinked"
    subdir = "jobs"
    key = payload['id']
    job = json.dumps(payload['job'])
    session = boto3.session.Session()
    client = session.client('batch')

    res = interlinked.store_item(key, job, bucket, subdir, gzip)

    res.body = client.submit_job(
        jobName = "zscore",
        jobQueue = "interlinked",
        jobDefinition = 'zscore:2',
        parameters={
            'string': 'string'
        },
        containerOverrides={
            'environment': [
                {
                    'name': 'LAMBDA_JOB_NAME',
                    'value': key
                },
            ]
        },
        timeout={
            'attemptDurationSeconds': 300
        }
    )
    return res
)