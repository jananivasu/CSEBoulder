"""Blob storage operation helper"""
import uuid
import base64
import io
from applicationinsights import TelemetryClient

from azure.storage.blob import BlockBlobService, PublicAccess

from oauth import AutoUpdatedTokenCredential
from settings import AZURE_STORAGE_ACCOUNT_NAME
from settings import APPINSIGHTS_INSTRUMENTATION_KEY
from settings import BLOB_CONTAINER_NAME


def UploadtoBlobStore(encodeddata: bytes, filetype: str, tc: TelemetryClient) -> int:
    """
    Function that instantiates the telemetry client and the appropriate block blob service and calls upload helper function with that parameters
    """
    # Create the BlockBlockService that is used to call the Blob service for the storage account
    with AutoUpdatedTokenCredential() as token_credential:
        block_blob_service = BlockBlobService(
            account_name=AZURE_STORAGE_ACCOUNT_NAME, token_credential=token_credential)

    container_name = BLOB_CONTAINER_NAME

    retval = doActualUpload(block_blob_service,container_name,encodeddata,filetype, tc)

    tc.flush()

    return retval


def doActualUpload(blockBlobService: BlockBlobService, containername:str, encodeddata:bytes, filetype:str, tc:TelemetryClient):
    """
    Actual function that creates a random filename and uploads to the blob storage
    """
    # Set the permission so the blobs are public.
    blockBlobService.set_container_acl(
        containername, public_access=PublicAccess.Container)

    # Create a filename using a random GUID
    upload_filename = "BoulderUpskill-"+str(uuid.uuid4())+"."+filetype

    # Extract the encoded base64 portion of the image from the request and convert to file
    encodedImage = io.BytesIO(base64.decodebytes(encodeddata))    

    # Upload to blob storage
    tc.track_trace(
        "\nUploading to Blob storage as blob with name: " + upload_filename)

     # Upload the created file, use upload_filename for the blob name
    try:
        blockBlobService.create_blob_from_stream(
            containername, upload_filename, encodedImage)
    except ValueError:
        return 500

    else:
        return 200  
