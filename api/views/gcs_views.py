# contrib

import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from server.settings import BASE_DIR
import json
import logging


# Models
from api.models.temporary_file_model import TemporaryFilesModel
from api.models.company_model import CompanyModel

from api.serializers.temporary_file_serializer import TempoaryFilesSerializer

# Helpers

from api.utils.helpers.helpers import get_file_name, gcs_custom_bucket_name


# server responses
from api.utils.server_responses.http_responses import (
    SUCCESS,
    SUCCESS_CODE,
    SERVER_ERROR,

)

from api.utils.gc_storage import (
    create_bucket,
    delete_cs_files,
    upload_cs_files,
    generate_presigned_cs_file_url

)


@api_view(["POST"])
def create_gcs_bucket(request, user):
    print("api.views.gcs_views.create_gcs_bucket()")
    try:
        COMPANY_ID = json.loads(request.body)["data"]["companyId"]
        COMPANY = CompanyModel.objects.filter(business_id=COMPANY_ID).first()
        # bucket_name = gcs_custom_bucket_name("COMPANY.business_name")
        bucket_name = gcs_custom_bucket_name(COMPANY.business_name)
        bucket_created = create_bucket(bucket_name)
        if bucket_created:
            return Response(
                {
                    "message": "Storage Name Created Successfully!",
                    "status": SUCCESS["STATUS"]
                },
                status=SUCCESS_CODE["STANDARD"]
            )
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"]
            },
            status=SERVER_ERROR["CODE"]
        )

    except Exception as error:
        print('api.views.gcs_views.create_gcs_bucket() error ->', error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )


@api_view(["POST"])
def upload_gcs_files(request, user):
    print("api.views.gcs_views.upload_gcs_files()")

    try:
        bucket_name = json.loads(request.POST.get('data'))["bucketName"]
        files = request.FILES.getlist('files')
        if not files:
            return Response({"error": "No files uploaded!"}, status=400)

        media_path = "media/uploads/"
        files_location = os.path.join(BASE_DIR, media_path)
        temp_files = []
        file_ids = []

        try:
            # saves files to django media path
            for file_obj in files:
                temp_file = TemporaryFilesModel.objects.create(file=file_obj)
                temp_files.append(temp_file.file.name)  # uploads/file_name.pdf
                file_ids.append({"file_id": temp_file.file_id})

            # returns a list of just the name of the files -> [some_files.pdf,some_files2.jpg]
            filenames = get_file_name(temp_files)
            # print(filenames)

            # uploads to gcs
            uploaded_files = upload_cs_files(
                bucket_name, filenames, files_location, media_path)
            # print(uploaded_files)

            if uploaded_files:
                # for each file uploaded to gcs successfully
                # create a presigned url or be availble to the public for a duration
                # This is for signalwire api purposes
                # Then updatethe file saved in the database with the presigned_url
                for item in file_ids:
                    file = TemporaryFilesModel.objects.get(
                        file_id=item["file_id"])
                    # print(file)
                    presigned_url = generate_presigned_cs_file_url(
                        bucket_name, f"media/{file.file.name}")
                    for key, value in presigned_url.items():
                        # print(item, key, value)
                        setattr(file, key, value)
                        file.save()

                # try to return the files with their presigned_url

                # uploaded_files = upload_cs_files(
                #     "media_some_thing", test, files_location, media_path)
                # print(uploaded_files)
                return Response(
                    {
                        "message": "SUCCESS",
                        "status": SUCCESS["STATUS"],
                    },
                    status=SUCCESS_CODE["CREATED"],
                )
            return Response(
                {
                    "message": SERVER_ERROR["MESSAGE"],
                    "status": SERVER_ERROR["STATUS"],
                },
                status=SERVER_ERROR["CODE"],
            )
        except Exception as error:
            print('uploaded file error ->', error)
            return Response(
                {
                    "message": SERVER_ERROR["MESSAGE"],
                    "status": SERVER_ERROR["STATUS"],
                },
                status=SERVER_ERROR["CODE"],
            )

    except Exception as error:
        print("api.views.gcs_views.upload_gcs_files() error -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )


@api_view(["GET"])
def get_all_gcs_files(request, user):
    print("api.views.gcs_views.get_all_gcs_files()")

    try:
        #  do logic heee
        DATA = json.loads(request.body)["data"]
        COMPANY_ID = DATA["companyId"]
        serializer = TempoaryFilesSerializer(
            TemporaryFilesModel.objects.filter(business_id=COMPANY_ID), many=True).data

        print("temporary files serializer", serializer)

        return Response(
            {
                "message": "SUCCESS",
                "data": serializer,
                "status": SUCCESS["STATUS"]
            },
            status=SUCCESS_CODE["STANDARD"]
        )

    except Exception as error:
        print("api.views.gcs_views.upload_gcs_files() error -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )


@api_view(["DELETE"])
def delete_gcs_files(request, user):
    print("api.views.gcs_views.delete_gcs_files()")

    try:
        FILES = json.loads(request.body)["data"]["files"]
        bucket_name = json.loads(request.body)["data"]["bucketName"]
        files_location = "media/uploads"

        files_to_delete = []

        for file in FILES:
            files_to_delete.append(f"{files_location}/{file["name"]}")

        deleted_files = delete_cs_files(bucket_name, files_to_delete)

        if deleted_files:
            for file in FILES:
                temp_file = TemporaryFilesModel.objects.filter(
                    file_id=file["file_id"]).first()
                temp_file.delete()

            return Response(
                {
                    "meesage": "Deleted Files Successfully!",
                    "status": SUCCESS["STATUS"]
                },
                status=SUCCESS_CODE["STANDARD"]
            )
        return Response(
            {
                "message": "Unable To Delete Files. Please try again later!",
                "status": SERVER_ERROR["STATUS"]
            },
            status=SERVER_ERROR["CODE"]
        )

    except Exception as error:
        print("api.views.gcs_views.delete_gcs_files() error -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )


@api_view(["GET"])
def get_gcs_files(request, user):
    print("api.views.gcs_views.get_gcs_file()")

    try:
        FILES = json.loads(request.body)["data"]["files"]
        # bucket_name = json.loads(request.body)["data"]["bucketName"] # need to re-think this approach
        serializer = []
        for file in FILES:
            # print(file)
            serialized_file = TempoaryFilesSerializer(
                TemporaryFilesModel.objects.filter(file_id=file["id"]), many=True).data[0]
            serializer.append(serialized_file)
        # print(serializer)

        return Response(
            {
                "message": "SUCCESS",
                "data": serializer,
                "status": SUCCESS["STATUS"]
            },
            status=SUCCESS_CODE["STANDARD"]
        )

    except Exception as error:
        print("api.views.gcs_views.delete_gcs_files() error -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )
