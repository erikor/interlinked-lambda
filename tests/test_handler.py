import unittest
import index
import upload
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
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn('Hello World', result['body'])

    def test_upload(self):
        print("testing upload.")
        result = upload.handler({"body" : '{"key": "1", "data": "[1,2,3,4,5]"}'}, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')

    def test_s3(self):
        data = [19, "A", 43, "B"]
        s3 = boto3.resource('s3')
        obj = s3.Object('interlinked','test/hello.tab')
        obj.put(Body='\n'.join(str(e) for e in data))
        obj = s3.Object('interlinked','test/hello.tab')
        data = obj.get()['Body'].read().decode('utf-8') 
        print("testing s3.")
        print data

if __name__ == '__main__':
    unittest.main()
