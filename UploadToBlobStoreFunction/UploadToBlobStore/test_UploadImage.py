"""Tests for UploadImageToBlobStore function"""
import unittest
import base64

import azure.functions as func

from main import run_functriggercode

from mockito import when, mock, unstub, verify, ANY


# To run this, run 'pytest'
# Pytest searches for files beginning with 'test_' and calls their main function.
# unittest.main() finds classes that inherit from 'unittest.TestCase', and run all functions whose names starts with 'test_'
class BlobUploadTest(unittest.TestCase):
    """Test class"""

    def test_func_1(self):
        r = func.HttpRequest
        imagedata = base64.b64encode(b'testdata')
        imageext = "jpg"

        PARAMS = {'image_data': imagedata, 'image_type' : imageext}

        r.params = PARAMS
       
        EXPECTED_BODYTEXT = "Successfully uploaded to blob store"
        EXPECTED_STATUSCODE = 200
    
        resp = run_functriggercode(r)

        print (resp.status_code)
        print (resp.get_body().decode('utf-8'))

        self.assertEqual(resp.status_code, EXPECTED_STATUSCODE, "")
        self.assertEqual(resp.get_body().decode('utf-8'), EXPECTED_BODYTEXT,"")

        unstub()


def runTest(self):
    self.test_func_1(self)
        

if __name__ == '__main__':
    unittest.main()
