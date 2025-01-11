from google.cloud import storage
from datetime import timedelta
import logging

# from api.utils.gc_storage.upload_cs_file import upload_cs_file


def generate_presigned_cs_file_url(bucket_name, blob_name, expiration_minutes=15):
    """
    Generate a pre-signed URL for a file in Google Cloud Storage.

    Args:
        bucket_name (str): The name of the GCS bucket.
        blob_name (str): The name of the file (object) in the bucket.
        expiration_minutes (int): How long the pre-signed URL is valid (default: 15 minutes).

    Returns:
        str: A pre-signed URL for the file.
    """
    try:
        # Initialize the storage client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        # Generate the pre-signed URL
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=expiration_minutes),
            method="GET",
        )

        # upload_cs_file(bucket_name,"/test/app_drive_test.pdf",)

        return url
    except Exception as error:
        print(
            "An Google Cloud Storage generate pre-signed cs file error occurred ->",
            error,
        )
        return False


# Example Usage
# bucket_name = "your-private-bucket"
# blob_name = "path/to/your-file.pdf"  # File path in the bucket
# expiration_minutes = 30  # URL will be valid for 30 minutes
# bucket_name = "media_some_thing"
# blob_name = "test/fax-service-system-django-e0168836712d.json"
# expiration_minutes = 30


# signed_url = generate_presigned_cs_file_url(bucket_name, blob_name, expiration_minutes)
# print("Pre-signed URL:", signed_url)
