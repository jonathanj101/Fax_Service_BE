from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv
from uuid import uuid4
import json
import logging
import jwt

# Modules
from api.models.company_model import CompanyModel
from api.models.user_model import UserModel
from api.serializers.company_serializer import CompanySerializer

# Helpers
from api.utils.server_responses.http_responses import (
    SUCCESS,
    SUCCESS_CODE,
    SERVER_ERROR,
    UN_AUTHORIZED,
    FORBIDEN_ACCESS,
    UNPROCESSIBLE_ENTITY,
)

# from api.utils.common.common import EMAIL_OWNER
from api.utils.helpers.helpers import split_bearer_value

# Auth
from api.utils.auth.jwt_auth import (
    create_access_jwtoken,
    decode_access_jwtoken,
    create_refresh_jwtoken,
)

# Loading environment variables
load_dotenv()

# unique id randominize
uid = uuid4()

# views in below here


@api_view(["POST"])
def register_company(request, user_model):
    print("api.views.company.register_company()")

    try:
        REQUEST_BODY = json.loads(request.body)
        COMPANY_DICT = {
            "business_name": REQUEST_BODY["businessName"],
            "business_street_address": REQUEST_BODY["businessStreetAddress"],
            "business_registered_country": REQUEST_BODY["businessRegisteredCountry"],
            "business_registered_city": REQUEST_BODY["businessRegisteredCity"],
            "business_registered_zipcode": REQUEST_BODY["businessRegisteredZipcode"],
            "business_contact_number": REQUEST_BODY["businessContactNumber"],
            "business_email": REQUEST_BODY["businessEmail"],
            "business_fax_number": REQUEST_BODY["businessFaxNumber"],
            "business_owner": REQUEST_BODY["businessOwner"],
            "business_type": REQUEST_BODY["businessType"],
            "business_size": REQUEST_BODY["businessSize"],
        }

        try:
            decoded_token = decode_access_jwtoken(token)
            USER = UserModel.objects.filter(user_id=user_model.user_id).first()
            if USER:
                try:
                    COMPANY = CompanyModel(
                        business_name=COMPANY_DICT["business_name"],
                        business_street_address=COMPANY_DICT["business_street_address"],
                        business_registered_country=COMPANY_DICT[
                            "business_registered_country"
                        ],
                        business_registered_city=COMPANY_DICT[
                            "business_registered_city"
                        ],
                        business_registered_zipcode=COMPANY_DICT[
                            "business_registered_zipcode"
                        ],
                        business_contact_number=COMPANY_DICT["business_contact_number"],
                        business_email=COMPANY_DICT["business_email"],
                        business_fax_number=COMPANY_DICT["business_fax_number"],
                        business_owner=USER,
                        business_type=COMPANY_DICT["business_type"],
                        business_size=COMPANY_DICT["business_size"],
                        # business_id="",
                    )
                    COMPANY.save()
                    serializer = CompanySerializer(
                        CompanyModel.objects.filter(
                            business_name=COMPANY_DICT["business_name"]
                        ),
                        many=True,
                    ).data[0]
                    print(serializer)
                    return Response(
                        {
                            "message": f"Company {COMPANY_DICT['business_name']} has been created successfully!",
                            "data": serializer,
                            "status": SUCCESS["STATUS"],
                            "status_code": SUCCESS_CODE["CREATED"],
                        }
                    )
                except Exception as exc:
                    print("An exception occurred -> ", exc)
                    logging.error(f"An Error Occurred -> ", exc)
                    return Response(
                        {
                            # "error": exc,
                            "message": SERVER_ERROR["MESSAGE"],
                            "status": SERVER_ERROR["STATUS"],
                            "status_code": SERVER_ERROR["CODE"],
                        }
                    )
        except jwt.exceptions.DecodeError as error:
            print("api.views.company_views.register_company()")
            logging.error("An Invalid Request Occurred", error)
            return Response(
                {
                    "error": error.user.message,
                    "message": SERVER_ERROR["MESSAGE"],
                    "status": SERVER_ERROR["STATUS"],
                    "status_code": SERVER_ERROR["CODE"],
                }
            )
    except (KeyError, TypeError) as error:
        print("api.views.company_views.register_company()")
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )


@api_view(["GET"])
def get_company(request, user_model):
    print("api.views.company.get_company()")
    # print(request.headers["Authorization"])
    try:
        DATA = json.loads(request.body)["data"]

        FILTER_COMPANY_ID = CompanySerializer(
            CompanyModel.objects.filter(business_id=DATA["company_id"]), many=True
        ).data[0]
        if FILTER_COMPANY_ID is not None:
            return Response(
                {
                    "message": "SUCCESS",
                    "data": FILTER_COMPANY_ID,
                    "status": SUCCESS["STATUS"],
                    "status_code": SUCCESS_CODE["STANDARD"],
                }
            )
        return Response(
            {
                "message": f"It seems that company does not exist within our record!",
                "status": SUCCESS["STATUS"],
                "status_code": SUCCESS_CODE["NOCONTENT"],
            }
        )

    except (KeyError, TypeError) as error:
        print("api.views.comapny_views.get_company()")
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )
    except (AssertionError, ValueError, AttributeError) as error:
        print("api.views.comapny_views.get_company()")
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )


@api_view(["PUT"])
def update_company(request, user_model):
    print("api.views.company_views.update_company()")
    DATA = json.loads(request.body)["data"]
    # print(request.headers)
    try:
        token = split_bearer_value(request.headers["Authorization"])
        decoded_token = decode_access_jwtoken(token)
        if decoded_token["isDecoded"]:
            COMPANY = CompanyModel.objects.get(business_id=id)
            FILTER_COMPANY_ID = CompanySerializer(
                CompanyModel.objects.filter(business_id=id), many=True
            ).data
            if COMPANY is not None:
                print("found company")
                for key, value in DATA.items():
                    setattr(COMPANY, key, value)
                    COMPANY.save()
                return Response(
                    {
                        "message": "SUCCESS",
                        "status": SUCCESS["STATUS"],
                        "status_code": SUCCESS_CODE["STANDARD"],
                    }
                )
            else:
                return Response(
                    {
                        "message": f"It seems that company does not exist within our record!",
                        "status": SUCCESS["STATUS"],
                        "status_code": SUCCESS_CODE["NOCONTENT"],
                    }
                )
        else:
            return Response(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    "status_code": UN_AUTHORIZED["CODE"],
                }
            )

    except (KeyError, TypeError) as error:
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )

    except (AttributeError, AssertionError) as error:
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
                "status_code": SERVER_ERROR["CODE"],
            }
        )
