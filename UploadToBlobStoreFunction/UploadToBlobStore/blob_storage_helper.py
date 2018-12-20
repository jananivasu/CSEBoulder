"""Blob storage operation helper"""
import uuid
import base64
import io
from applicationinsights import TelemetryClient
from azure.storage.blob import BlockBlobService

def upload_to_blobstore(block_blob_service, container_name, encoded_data: bytes, file_ext: str, telemetry_client: TelemetryClient) -> int:
    """
    Function that instantiates the telemetry client and the appropriate block blob service 
    and calls upload helper function with that parameters
    """
    telemetry_client.track_trace("Calling function to build filename and upload...")
    upload_result_statuscode = build_filename_and_upload(block_blob_service, container_name, encoded_data, file_ext, telemetry_client)
    telemetry_client.flush()

    return upload_result_statuscode

def build_filename_and_upload(block_blob_service:BlockBlobService, container_name:str, encoded_data:bytes, file_ext:str, telemetry_client:TelemetryClient) -> int:
    """
    Actual function that creates a random filename and uploads to the blob storage
    """
    # Create a filename using a random GUID
    upload_filename = "BoulderUpskill-"+str(uuid.uuid4())+"."+file_ext

    # Extract the encoded base64 portion of the image from the request and convert to file
    encoded_image = io.BytesIO(base64.decodebytes(encoded_data))    

    # Upload to blob storage
    telemetry_client.track_trace(
        "\nUploading to Blob storage as blob with name: " + upload_filename)

    telemetry_client.flush()

     # Upload the created file, use upload_filename for the blob name
    try:
        block_blob_service.create_blob_from_stream(
            container_name, upload_filename, encoded_image)
    except ValueError:
        return 500
    else:
        return 200  
