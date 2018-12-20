"""Tests for UploadImageToBlobStore function"""
import unittest
import base64
import azure.functions as func
from azure.storage.blob import BlockBlobService
from applicationinsights import TelemetryClient
from mockito import unstub, when, ANY, mock, verify
from main import run_functriggercode

# To run this, run 'pytest'
# Pytest searches for files beginning with 'test_' and calls their main function.
# unittest.main() finds classes that inherit from 'unittest.TestCase',
# and run all functions whose names starts with 'test_'
class BlobUploadTest(unittest.TestCase):
    """Test to verify function code that extracts image
       & type from request and calls mock upload
    """

    def test_func_upload(self):
        """
        Test the HTTP trigger function code to upload image
        """
        # Use test encoded data and a test file ext
        test_image_data = base64.b64encode(b'testdata')
        test_image_ext = "jpg"

        # Create a http request for passing in
        http_request = func.HttpRequest

        # Pass in the encoded image and ext to the request as params
        http_params = {'image_data': test_image_data, 'image_type': test_image_ext}
        http_request.params = http_params

        # Define expected http response
        expected_http_response = "Successfully uploaded to blob store"
        expected_http_statuscode = 200

        # Create mock telemetry client and stub methods to use in func call
        mock_telemetry_client = mock(TelemetryClient)
        when(mock_telemetry_client).track_trace(any).thenReturn(print(''))
        when(mock_telemetry_client).flush().thenReturn()

        # Create mock block blob service and stub upload method to use in func call
        mock_blobservice = BlockBlobService("testaccount", "testkey")
        when(mock_blobservice).create_blob_from_stream(any, any, any).thenReturn(True)

        # Create mock blob container name
        mock_container_name = "test"

        # Call the func with actual func trigger code with mock params
        http_response = run_functriggercode(mock_blobservice, mock_container_name,\
                                              http_request, mock_telemetry_client)

        print(http_response.status_code)
        print(http_response.get_body().decode('utf-8'))

        # Assert that we got the expected output
        self.assertEqual(http_response.status_code, expected_http_statuscode, "")
        self.assertEqual(http_response.get_body().decode(
            'utf-8'), expected_http_response, "")

        # Verify that upload to blob store was called once from inside the func
        verify(mock_blobservice, times=1).create_blob_from_stream(any, any, any)
        verify(mock_telemetry_client, times=6).track_trace(any)

        unstub()

    def runTest(self):
        """
        The main run test method for the unittest class
        """
        self.test_func_upload()


if __name__ == '__main__':
    unittest.main()
