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
        result = model.store({"body" : '{"bucket": "interlinked",' +
                                            '"key": "1", ' +
                                            '"gzip": "true", ' +
                                            '"subdir": "test", ' +
                                            '"data": [1,2,3,4,5]}'}, None)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

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
