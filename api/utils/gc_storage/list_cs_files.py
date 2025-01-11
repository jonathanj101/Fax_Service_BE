import os
import logging
from google.cloud import storage
from dotenv import load_dotenv


load_dotenv()


# print(os.environ[""])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
]


def list_cs_files(bucket_name):
    try:

        storage_client = storage.Client()

        file_list = storage_client.list_blobs(bucket_name)
        file_list = [file.name for file in file_list]

        return file_list
    except Exception as error:
        print("An Google Cloud Storage error occurred ->", error)
        logging.error("An Google Cloud Storage list of files error occurred ->", error)
        return False


# print(list_cs_files("media_some_thing"))
