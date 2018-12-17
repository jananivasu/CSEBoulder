"""
Set of tests for OCR services
"""

import unittest

from mockito import when, ANY, verify

from ..shared.ocr_shared import AzureOcrService
from ..UploadOcrTrigger import run_ocr

class TestOcrTrigger(unittest.TestCase):
    """
    Runs Ocr Trigger Tests
    """

    def test_run_ocr(self):
        """
        Validates run_ocr
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
            .get_ocr_results(ANY,
                             ANY,
                             ANY) \
            .thenReturn(ocr_json)

        actual_output = run_ocr(AzureOcrService(),
                                "http://ocrservice",
                                "key0",
                                "http://blob/image1.jpg")

        expected_output = " A Good Boy"

        self.assertEqual(expected_output, actual_output, "Expected wasn't equal to actual")

        verify(AzureOcrService, times=1).get_ocr_results(ANY, ANY, ANY)
