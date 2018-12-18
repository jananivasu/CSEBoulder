"""
Azure HTTP trigger function module
"""
import logging
import azure.functions as func

from applicationinsights import TelemetryClient

from BlobStorageHelper import UploadtoBlobStore


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure function for HTTP trigger
    """
    # Create the telemetry client instance
    tc = TelemetryClient(APPINSIGHTS_INSTRUMENTATION_KEY)

    tc.track_trace("Python HTTP trigger function processed a request.")

    # Extract the filetype from the request
    filetype = req.params.get('image_type')

    if not filetype:
        tc.track_trace("Could not find the file type as part of the HTTP request body")
        tc.flush()
        return func.HttpResponse(
            "Could not find the file type as part of the HTTP request body",
            status_code=400
        )

    # Extract the encoded base64 portion of the image & image type from the request
    encodedImage = req.get_body()
    #encodedImage = req.params.get('image_data')

    if not encodedImage:
        tc.track_trace("Could not find encoded image as part of the HTTP request body")
        tc.flush()
        return func.HttpResponse(
            "Could not find encoded image as part of HTTP request body",
            status_code=400
        )

    # Upload to blob storage
    retval = UploadtoBlobStore(encodedImage, filetype)

    if retval == 200:
        tc.track_trace("Successfully uploaded to blob store")
        tc.flush()
        return func.HttpResponse(
            "Successfully uploaded to blob store",
            status_code=200
        )

    else:
        tc.track_trace("Error occurred while uploading to blob store")
        tc.flush()
        return func.HttpResponse(
            "Error occurred while uploading to blob store",
            status_code=500
        )

def run_functriggercode(req: func.HttpRequest) -> func.HttpResponse:
    # Extract the encoded base64 portion of the image & image type from the request
    encodedImage = req.params.get('image_data')
    print (encodedImage)

    if not encodedImage:
        return func.HttpResponse(
            "Could not find encoded image as part of HTTP request body",
                status_code=400
        )
    # Extract the filetype from the request
    filetype = req.params.get('image_type')
    print (filetype)

    if not filetype:
        return func.HttpResponse(
            "Could not find the file type as part of the HTTP request body",
            status_code=400
        )
  
    return func.HttpResponse(
            "Successfully uploaded to blob store",
            status_code=200
    )
