"""
Module for OCR upload trigger scenario.
"""

import logging

import azure.functions as func

def main(myblob: func.InputStream):
    """
    Main entry point for image OCR processing when new image is uploaded.
    """
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
