"""
Module for OCR upload trigger scenario.
"""

import os
import logging
import json
import azure.functions as func
from ..shared.ocr_shared import AzureOcrService

ocr_service_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/ocr"
blob_base_url = "https://boulderupskillstorage.blob.core.windows.net/"
subscription_key = os.getenv('OCR_SUBSCRIPTION_KEY')

def main(triggeredblob: func.InputStream, doc: func.Out[func.Document]):
    """
    Main entry point for image OCR processing when new image is uploaded.
    """
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {triggeredblob.name}\n"
                 f"Blob Size: {triggeredblob.length} bytes")

    blob_path = blob_base_url + triggeredblob.name

    # TODO: Input validation, although what to do with bad input?
    # Blob trigger functions don't support HTTP responses.

    OcrService = AzureOcrService()
    results = OcrService.get_ocr_results(ocr_service_url, subscription_key, blob_path)
    output_text = OcrService.format_ocr_text(results)

    outdata = {"ocr_text": output_text}
    doc.set(func.Document.from_json(json.dumps(outdata)))
