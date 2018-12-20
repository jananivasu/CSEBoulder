"""
Azure HTTP trigger function module
"""
from applicationinsights import TelemetryClient
import azure.functions as func
from azure.storage.blob import BlockBlobService, PublicAccess
from oauth import AutoUpdatedTokenCredential
from .blob_storage_helper import upload_to_blobstore
from .settings import APPINSIGHTS_INSTRUMENTATION_KEY,\
 AZURE_STORAGE_ACCOUNT_NAME, BLOB_CONTAINER_NAME

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure function for HTTP trigger
    """
    # Create the telemetry client instance
    telemetry_client = TelemetryClient(APPINSIGHTS_INSTRUMENTATION_KEY)
    telemetry_client.track_trace("Python HTTP trigger function processed a request.")

    # Create the BlockBlockService that is used to call the Blob service for the storage account
    telemetry_client.track_trace("Setting up blob container for upload")
    with AutoUpdatedTokenCredential() as token_credential:
        block_blob_service = BlockBlobService(
            account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential)
    container_name = BLOB_CONTAINER_NAME

    # Set the permission so the blobs are public.
    telemetry_client.track_trace("Setting up public access for blob container")
    block_blob_service.set_container_acl(
        container_name, public_access=PublicAccess.Container)


    # Call the helper function to process request
    http_response = run_functriggercode(block_blob_service, container_name, req, telemetry_client)
    telemetry_client.flush()
    return http_response


def run_functriggercode(block_blob_service: BlockBlobService, container_name: str, \
    req: func.HttpRequest, telemetry_client: TelemetryClient) -> func.HttpResponse:
    """
    The core logic of the function to parse and upload to blob store
    (separated out for testability)
    """
    # Extract the encoded base64 portion of the image & image type from the request
    telemetry_client.track_trace("Extracting encoded image from request")
    encoded_image = req.params.get('image_data')
    if not encoded_image:
        return func.HttpResponse(
            "Could not find encoded image as part of HTTP request body",
            status_code=400
        )

    # Extract the filetype from the request
    telemetry_client.track_trace("Extracting file extension from request")
    file_ext = req.params.get('image_type')
    if not file_ext:
        return func.HttpResponse(
            "Could not find the file ext as part of the HTTP request body",
            status_code=400
        )
    # Upload to blob storage
    telemetry_client.track_trace("Calling upload_to_blobstore...")
    blob_upload_result = upload_to_blobstore(block_blob_service, container_name, \
    encoded_image, file_ext, telemetry_client)
    if blob_upload_result == 200:
        telemetry_client.track_trace("Successfully uploaded to blob store")
        telemetry_client.flush()
        return func.HttpResponse(
            "Successfully uploaded to blob store",
            status_code=200
        )

    telemetry_client.track_trace("Error occurred while uploading to blob store")
    telemetry_client.flush()
    return func.HttpResponse(
        "Error occurred while uploading to blob store",
        status_code=500
    )
