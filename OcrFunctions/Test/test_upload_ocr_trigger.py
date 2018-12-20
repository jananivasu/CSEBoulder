"""
Set of tests for OCR services
"""

import unittest

from mockito import when, ANY, verify

from ..shared.ocr_shared import AzureOcrService
from ..UploadOcrTrigger import process_image

class TestOcrTrigger(unittest.TestCase):
    """
    Runs Ocr Trigger Tests
    """

    def test_process_image(self):
        """
        Validates process_image
        """

        ocr_json = {
            "regions": [
                {
                    "lines": [
                        {
                            "words": [
                                {
                                    "text": "A"
                                },
                                {
                                    "text": "Good"
                                },
                                {
                                    "text": "Boy"
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        when(AzureOcrService) \
            .get_ocr_results(ANY) \
            .thenReturn(ocr_json)

        TestOcrService = AzureOcrService("http://ocrservice", "key0")
        expected_output = "A Good Boy"
        actual_output = process_image(TestOcrService,
                                      "http://blob/image1.jpg")

        self.assertEqual(expected_output, actual_output, "Expected wasn't equal to actual")

        verify(AzureOcrService, times=1).get_ocr_results(ANY)
