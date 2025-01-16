import os
from google.cloud import storage
from google.cloud.storage import transfer_manager
import logging
from dotenv import load_dotenv

load_dotenv()


# print(os.environ[""])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
]


# def download_cs_files(bucket_name, file_name, destination_file_name):
#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     blob.download_to_filename(destination_file_name)

#     return True


def download_cs_files(bucket_name, filenames, destination):

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        results = transfer_manager.download_many_to_path(
            bucket, filenames, destination)
        return True
    except Exception as error:
        print("An Google Cloud Storage download files error occurred ->", error)
        logging.error(
            "An Google Cloud Storage download files error occured -> ", error)
        return False


# download_cs_files(
#     "media_some_thing",
#     ["test/app_driver_test.pdf", "test/fax-service-system-django-e0168836712d.json"],
#     "/home/jonathan/Documents/Python_Projects/Fax_Service_System/Fax_Service_Server/api/utils/gc_storage/",
# )
