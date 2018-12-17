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

def main(triggered_blob: func.InputStream, doc: func.Out[func.Document]):
    """
    Main entry point for image OCR processing when new image is uploaded.
    """
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {triggered_blob.name}\n"
                 f"Blob Size: {triggered_blob.length} bytes")

    blob_path = blob_base_url + triggered_blob.name

    # TODO: Input validation, although what to do with bad input?
    # Blob trigger functions don't support HTTP responses.
    ocr_service = AzureOcrService()
    output_text = run_ocr(ocr_service, ocr_service_url, blob_path, subscription_key)

    outdata = {"ocr_text": output_text}
    doc.set(func.Document.from_json(json.dumps(outdata)))

def run_ocr(ocr_service: AzureOcrService, service_url: str, key: str, blob_path: str) -> str:
    """
    Executes OCR
    """
    results = ocr_service.get_ocr_results(service_url, key, blob_path)
    output_text = ocr_service.process_ocr_text(results)

    return output_text
