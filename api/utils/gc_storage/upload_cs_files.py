from google.cloud import storage
from google.cloud.storage import transfer_manager
from dotenv import load_dotenv
import os

load_dotenv()


# print(os.environ[""])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
]


# def upload_cs_file(bucket_name, source_file_name, destination_file_name):
#     storage_client = storage.Client()

#     bucket = storage_client.bucket(bucket_name)

#     blob = bucket.blob(destination_file_name)
#     blob.upload_from_filename(source_file_name)

#     return True


def upload_cs_files(bucket_name, filenames, blob_name_prefix, source_directory):
    # print(BASE_DIR)
    # for file in blob_name_prefix:
    #     print(file)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    results = transfer_manager.upload_many_from_filenames(
        bucket, filenames, blob_name_prefix, source_directory
    )

    # print(results, "results")

    for name, result in zip(filenames, results):
        # The results list is either `None` or an exception for each filename in
        # the input list, in order.

        if isinstance(result, Exception):
            print("Failed to upload {} due to exception: {}".format(name, result))
            return False
        else:
            print("Uploaded {} to {}.".format(name, bucket.name))

    return True


# upload_cs_files(
#     "media_some_thing",
#     [
#         "app_driver_test.pdf",
#         "fax-service-system-django-e0168836712d.json",
#     ],
#     "/home/jonathan/Documents/Python_Projects/Fax_Service_System/Fax_Service_Server/api/utils/gc_storage/",
#     "test/",
# )
# source_directory = "path/name/to/upload/files/to"
# blob_name_prefix = "path/to/directory/where/files/are/located"
