import os
import logging
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()


# print(os.environ[""])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
]


def create_bucket(bucket_name, storage_class="STANDARD", location="us"):

    try:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)
        bucket.storage_class = storage_class

        bucket = storage_client.create_bucket(bucket, location=location)
        print(f"Bucket {bucket.name} successfully created.")
        return True
    except Exception as error:
        print("An Google Cloud Storage error occurred ->", error)
        logging.error(
            "An Google Cloud Storage bucket creation error occurred -> ", error
        )
        print(f"Bucket {bucket.name} not created, an error occurred")
        return False


# create_bucket("media_some_thing")
