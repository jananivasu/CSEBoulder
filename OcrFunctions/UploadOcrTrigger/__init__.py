"""
Module for OCR upload trigger scenario.
"""

import logging
import json
import azure.functions as func

# TODO: The follwing imports are producing errors
# from .shared import ocr_shared
# from ocr_shared import AzureOcrService, BlobStorageService, processImage

DEFAULT_RETURN_HEADER = {"content-type": "application/json"}

def main(myblob: func.InputStream, doc: func.Out[func.Document]):
    """
    Main entry point for image OCR processing when new image is uploaded.
    """
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")

    # Input validation, although what to do with bad input?
    # Blob trigger functions seemingly don't support HTTP responses.

    # ocr_service = AzureOcrService()
    # storage_service = BlobStorageService()
    # status = processImage(myblob, ocr_service, storage_service, doc)

    # Test writing some output to the cosmos DB
    outdata = {"test": myblob.name}
    doc.set(func.Document.from_json(json.dumps(outdata)))

    '''
    # Note: Blob trigger functions seemingly don't support HTTP responses.
    # return func.HttpResponse(
    #     status_code=200,
    #     headers=DEFAULT_RETURN_HEADER,
    #     body=json.dumps({"success": "success"})
    # )
    '''
