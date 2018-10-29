import unittest
import index
import model
import sys
try:
    import boto3
except ImportError:
    sys.path.append('lib')
    import boto3
import json

class TestHandlerCase(unittest.TestCase):
    
    def test_response(self):
        print("testing response.")
        result = index.handler(None, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('Hello World', result['body'])

    def test_model(self):
        print("testing upload.")
        result = model.store({"body": '{"key":"2","data":[4.1999,4.6232,12.495,6.8865,8.9907],"subdir":"test", "bucket":"interlinked"}'}, None)
        result = model.store({"body" : '{"bucket": "interlinked",' +
                                            '"key": "1", ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test", ' +
                                            '"data": [1,2,3,4,5]}'}, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        
        print("testing bulk upload.")
        result = model.bulk({"body" : '{"bucket": "interlinked",' +
                                            '"keys": ["1", "2", "3"], ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test", ' +
                                            '"data": [[1,2,3,4,5],[1,2,3,4,5],[1,2,3,4,5]]}'}, None)

        print("testing download.")
        result = model.fetch({"body" : '{"bucket": "interlinked",' +
                                            '"key": "1", ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test"}'}, None)
        data = json.loads(result['body'])
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(data[0], 1)

if __name__ == '__main__':
    unittest.main()
