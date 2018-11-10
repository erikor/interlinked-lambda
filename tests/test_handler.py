import unittest
import index
import model
import batch
import sys
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json

#python -m unittest discover tests
class TestHandlerCase(unittest.TestCase):
    def test_auth(self):
        print("testing connectivity.")
        result = model.fetch({"body" : '{"bucket": "interlinked",' +
                                            '"key": "2", ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test"}'}, None)
        data = json.loads(result['body'])
        self.assertEqual(result['statusCode'], 200)
   
    def test_model(self):
   
        print("testing upload.")
        result = model.store({"body": '{"key":"1","data":[4.1999,4.6232,12.495,6.8865,8.9907],"subdir":"test", "bucket":"interlinked"}'}, None)
        result = model.store({"body" : '{"bucket": "interlinked",' +
                                            '"key": "2", ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test", ' +
                                            '"data": [1,2,3,4,5]}'}, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        result = model.store({"body" : '{"bucket": "nosuchbucket", "key": "2", "data": [1,2,3,4,5]}'}, None)
        self.assertEqual(result['statusCode'], 501)
        
        print("testing check exists.")
        result = model.check({"body": '{"key":"foobar","subdir":"test", "bucket":"interlinked"}'}, None)
        self.assertEqual(result['statusCode'], 404)
        result = model.store({"body": '{"key":"1","data":[4.1999,4.6232,12.495,6.8865,8.9907],"subdir":"test", "bucket":"interlinked", "overwrite":false}'}, None)
        #self.assertEqual(result['statusCode'], 202)

        print("testing bulk upload.")
        result = model.bulk({"body" : '{"bucket": "interlinked",' +
                                            '"keys": ["6", "7", "8"], ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test", ' +
                                            '"overwrite": false, ' +
                                            '"data": [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]}'}, None)
        result = model.bulk({"body" : '{"bucket": "interlinked",' +
                                            '"keys": ["6", "7", "8"], ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test", ' +
                                            '"overwrite": false, ' +
                                            '"data": [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]}'}, None)
        res = json.loads(result['body'])
        self.assertEqual(res['pre_existing_objects'], 3)

        print("testing download.")
        result = model.fetch({"body" : '{"bucket": "interlinked",' +
                                            '"key": "2", ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test"}'}, None)

        data = json.loads(result['body'])
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(data[0], 1)

    def test_logging(self):   
        print("testing logging.")
        result = model.log({"body": '{"message": "Testing logging 1", "level": "INFO", "bucket":"interlinked"}'}, None)
        self.assertEqual(result['statusCode'], 200)
        result = model.log({"body": '{"message": "Testing logging 2", "level": "INFO", "bucket":"interlinked"}'}, None)
        self.assertEqual(result['statusCode'], 200)
        result = model.log({"body": '{"message": "Testing logging 2", "level": "ERROR", "bucket":"interlinked"}'}, None)
        self.assertEqual(result['statusCode'], 200)

    def test_submit(self):
        print("testing job submission.")
        result = batch.submit({"body" : '{"debug": true, "name": "lambda test 1", "func": "myfunc",' +
                                         '"script": "test.r",' +
                                         '"arguments": {"a": 1, "b": 2}}'}, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
if __name__ == '__main__':
    unittest.main()
