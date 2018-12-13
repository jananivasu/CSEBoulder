"""
Shared code for OCR functions and storage manipulation.
"""

class AzureOcrService:
    """
    Class for OCR service.
    """
    # process function - takes in blob, returns output text (decide format)
    pass

class BlobStorageService:
    """
    Class for storage services and manipulation.
    """
    # save function - takes in text and location to save to, saves as .txt file
    # (for now, look at adding other formats later)
    # returns status code indicating whether save succeeded or failed
    pass

def processImage(blob, OcrService, StorageService, doc):
    """
    Function that makes use of AzureOcrService and BlobStorageService classes to
    process an image, extract the text, and store it as an output file.
    """
    pass
    # input validation
    # text = OcrService.process(blob)
    # validate text, return bad status code if empty
    # status = storageService.save(text, doc)
    # return status
