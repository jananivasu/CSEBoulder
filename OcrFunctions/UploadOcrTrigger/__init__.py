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
    logging.info("Python blob trigger function processed blob.")
    logging.info(f"Name: {triggeredblob.name}")
    logging.info(f"Blob Size: {triggeredblob.length} bytes")

    blob_path = blob_base_url + triggeredblob.name
    image_name = triggeredblob.name.split('/')[-1]

    # TODO: Input validation, although what to do with bad input?
    # Blob trigger functions don't support HTTP responses.

    OcrService = AzureOcrService(ocr_service_url, subscription_key)
    output_text = process_image(OcrService, blob_path)

    outdata = {"image_url": blob_path,
               "image_name": image_name,
               "ocr_text": output_text
               }
    doc.set(func.Document.from_json(json.dumps(outdata)))

def process_image(OcrService, blob_path):
    """
    Function to run OCR against an input blob, and return the text as a string.
    """
    ocr_analysis = OcrService.get_ocr_results(blob_path)
    output_text = OcrService.format_ocr_text(ocr_analysis)
    return output_text
