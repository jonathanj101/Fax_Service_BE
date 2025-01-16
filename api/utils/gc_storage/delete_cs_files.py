import os
import logging

from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()


# print(os.environ[""])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
]


def delete_cs_files(bucket_name, files):

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        deleted_files = bucket.delete_blobs(files)
        # print(deleted_files)
        return True
    except Exception as error:
        print("An Google Cloud Storage delete files error occurred ->", error)
        logging.error("An Google Cloud Storage error occurred -> ", error)
        return False


# delete_cs_files("media_some_thing", ["test/test.json"])
