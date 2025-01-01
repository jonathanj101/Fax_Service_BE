# contrib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from dotenv import load_dotenv
import uuid
import json
import logging
import jwt
from django.core.exceptions import FieldError

# Modules
from api.models.employee_model import EmployeeModel
from api.serializers.employee_serializer import EmployeeSerializer
from api.models.company_model import CompanyModel
from api.models.user_model import UserModel

# Helpers
from api.utils.helpers.helpers import split_bearer_value
from api.utils.server_responses.http_responses import (
    SUCCESS,
    SUCCESS_CODE,
    SERVER_ERROR,
    UN_AUTHORIZED,
    FORBIDEN_ACCESS,
    UNPROCESSIBLE_ENTITY,
)

# Auth
from api.utils.auth.jwt_auth import decode_access_jwtoken

# Loading environment variables
load_dotenv()


@api_view(["POST"])
def create_employee(request, user_model):
    print("api.views.employee_views.create_employee()")

    try:
        REQUEST_BODY = json.loads(request.body)
        DATA = {
            "business_id": REQUEST_BODY["companyId"],
            "user_id": REQUEST_BODY["userId"],  # user model id, to grab user data
        }

        try:
            business = CompanyModel.objects.filter(
                business_id=DATA["business_id"]
            ).first()

            EMPLOYEE = EmployeeModel(
                company_id=business.business_id, user_id=DATA["user_id"]
            )
            # print(type(business.business_id))
            EMPLOYEE.save()
            serializer = EmployeeSerializer(
                EmployeeModel.objects.filter(
                    company_id=business.business_id, user_id=DATA["user_id"]
                ),
                many=True,
            ).data

            return Response(
                {
                    "message": "SUCCESS",
                    "data": serializer,
                    "status": SUCCESS["STATUS"],
                },
                status=SUCCESS_CODE["STANDARD"],
            )

        except FieldError as error:
            print("An exception occurred")
            logging.error("An Invalid Request Occurred", error)
            return Response(
                {
                    "message": SERVER_ERROR["MESSAGE"],
                    "status": SERVER_ERROR["STATUS"],
                },
                status=SERVER_ERROR["CODE"],
            )

    except (KeyError, TypeError) as error:
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
            },
            status=UN_AUTHORIZED["CODE"],
        )

    except (AttributeError, AssertionError) as error:
        logging.error("An Invalid Request Occurred", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )


@api_view(["GET"])
def get_employees_by_company_id(request):
    print("api.views.employee_views.get_employee_by_company_id()")
    try:
        DATA = json.loads(requesst.body)["data"]
        EMPLOYEES = EmployeeModel.objects.filter(
            company_id=uuid.UUID(DATA["company_id"])
        ).first()
        serializer = EmployeeSerializer(
            EmployeeModel.objects.filter(company_id=DATA["company_id"]), many=True
        ).data

        return Response(
            {
                "message": "SUCCESS",
                "data": serializer,
                "status": SUCCESS["STATUS"],
            },
            status=SUCCESS_CODE["STANDARD"],
        )
        # to do - > need more errors handling
    except (KeyError, TypeError) as error:
        logging.error("An Error Occurred -> ", error)

        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
            },
            status=UN_AUTHORIZED["CODE"],
        )
    except ValueError as error:
        logging.error("An Error Occurred -> ", error)

        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
            },
            status=UNPROCESSIBLE_ENTITY["CODE"],
        )


@api_view(["POST"])
def update_employee_status(request, USER):
    print("api.views.employee_views.update_employee_status()")
    try:
        DATA = json.loads(request.body)["data"]
        user_id = DATA["user_id"]
        update_data = DATA["update_data"]
        EMPLOYEE = EmployeeModel.objects.get(user_id=user_id)
        if EMPLOYEE is not None:

            for key, value in update_data.items():
                setattr(EMPLOYEE, key, value)
                EMPLOYEE.save()
                return Response(
                    {
                        "message": "SUCCESS",
                        "status": SUCCESS["STATUS"],
                    },
                    status=SUCCESS_CODE["STANDARD"],
                )

    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
            },
            status=UNPROCESSIBLE_ENTITY["CODE"],
        )

    except (AssertionError, ValueError, AttributeError) as error:
        print("An AssertionError or ValueError, AttributeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
            },
            status=UN_AUTHORIZED["CODE"],
        )


# testing view
# @api_view(["GET"])
# def get_employee_by_company_id(request, company_id):
#     employee = EmployeeSerializer(
#         EmployeeModel.objects.filter(company_id=uuid.UUID(company_id)), many=True
#     ).data
#     print(employee)

#     return Response({"data": employee})
