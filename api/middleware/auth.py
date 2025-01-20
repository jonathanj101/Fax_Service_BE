import django
import json
from django.http import JsonResponse
from api.utils.auth.jwt_auth import decode_access_jwtoken
from api.utils.helpers.helpers import split_bearer_value
from api.utils.server_responses.http_responses import (
    UN_AUTHORIZED,
    UNPROCESSIBLE_ENTITY,
)
import logging

from api.models.user_model import UserModel


# auth middleware to authenticate users (registered users, employees, businessowner) before accessing views
def auth_middleware(get_response):
    print("Users Auth Middleware Initialized")

    def wrapped_view(request):
        # print(request.COOKIES)
        # print(request)
        try:
            # print(request.headers["Authorization"])
            # excluded_paths = [
            #     "/api/fax-services/list-all-fax"
            # ]
            # if request.path in excluded_paths:
            #     return get_response(request)
            if request.headers["Authorization"]:
                token = split_bearer_value(request.headers["Authorization"])
                decoded_token = decode_access_jwtoken(token)
                if decoded_token["isDecoded"]:
                    USER = UserModel.objects.filter(
                        user_id=decoded_token["payload"]
                    ).first()
                    if USER is not None:

                        return get_response(request, USER)
                    return JsonResponse(
                        {
                            "message": UN_AUTHORIZED["MESSAGE"],
                            "status": UN_AUTHORIZED["STATUS"],
                            # "status_code": UN_AUTHORIZED["CODE"],
                        },
                        status=UN_AUTHORIZED["CODE"],
                    )
                else:
                    return JsonResponse(
                        {
                            "message": UN_AUTHORIZED["MESSAGE"],
                            "status": UN_AUTHORIZED["STATUS"],
                            # "status_code": UN_AUTHORIZED["CODE"],
                        },
                        status=UN_AUTHORIZED["CODE"],
                    )
                    # return Response(
                    #     {
                    #         "message": UN_AUTHORIZED["MESSAGE"],
                    #         "status": UN_AUTHORIZED["STATUS"],
                    #         "status_code": UN_AUTHORIZED["CODE"],
                    #     },
                    #     status=401,
                    # )
        except KeyError as error:
            logging.error("KeyError Occurred ", error)

            # return Response(
            #     {
            #         "message": UN_AUTHORIZED["MESSAGE"],
            #         "status": UN_AUTHORIZED["STATUS"],
            #         "status_code": UN_AUTHORIZED["CODE"],
            #     },
            #     status=401,
            # )

            return JsonResponse(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    # "status_code": UN_AUTHORIZED["CODE"],
                },
                status=UN_AUTHORIZED["CODE"],
            )

        except (
            django.http.request.RawPostDataException,
            json.decoder.JSONDecodeError,
        ) as error:
            logging.error("Unexpected error occurred in auth middleware")
            return JsonResponse(
                {
                    "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                    "status": UNPROCESSIBLE_ENTITY["STATUS"],
                    # "status_code": UNPROCESSIBLE_ENTITY["CODE"],
                },
                status=UNPROCESSIBLE_ENTITY["CODE"],
            )
        except Exception as error:
            logging.error(
                "Unexpected error occurred in auth middleware", exc_info=True)
            # return Response(
            #     {
            #         "message": "An unexpected error occurred",
            #         "status": "Error",
            #         "status_code": 500,
            #     },
            #     status=500,
            # )
            return JsonResponse(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    # "status_code": UN_AUTHORIZED["CODE"],
                },
                status=UN_AUTHORIZED["CODE"],
            )

    return wrapped_view


# admin auth middleware to authenticate valid admin users only
def admin_auth_middleware(get_response):
    print("Admin Auth Middleware Initialized")

    def wrapped_view(request):
        try:
            if request.headers["Authorization"]:
                token = split_bearer_value(request.headers["Authorization"])
                decoded_token = decode_access_jwtoken(token)
                if decoded_token["isDecoded"]:
                    USER = UserModel.objects.filter(
                        user_id=decoded_token["payload"]
                    ).first()
                    if USER is not None and USER.role == "super-admin":
                        print("user authenticated")
                        return get_response(request, USER)
                    #   un authenticated user
                    return JsonResponse(
                        {
                            "message": UN_AUTHORIZED["MESSAGE"],
                            "status": UN_AUTHORIZED["STATUS"],
                            # "status_code": UN_AUTHORIZED["CODE"],
                        },
                        status=UN_AUTHORIZED["CODE"],
                    )
                return JsonResponse(
                    {
                        "message": UN_AUTHORIZED["MESSAGE"],
                        "status": UN_AUTHORIZED["STATUS"],
                        # "status_code": UN_AUTHORIZED["CODE"],
                    },
                    status=UN_AUTHORIZED["CODE"],
                )
        except KeyError as error:
            logging.error("KeyError Occurred ", error)

            # return Response(
            #     {
            #         "message": UN_AUTHORIZED["MESSAGE"],
            #         "status": UN_AUTHORIZED["STATUS"],
            #         "status_code": UN_AUTHORIZED["CODE"],
            #     },
            #     status=401,
            # )

            return JsonResponse(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    # "status_code": UN_AUTHORIZED["CODE"],
                },
                status=UN_AUTHORIZED["CODE"],
            )

        except (
            django.http.request.RawPostDataException,
            json.decoder.JSONDecodeError,
        ) as error:
            logging.error("Unexpected error occurred in auth middleware")
            return JsonResponse(
                {
                    "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                    "status": UNPROCESSIBLE_ENTITY["STATUS"],
                    # "status_code": UNPROCESSIBLE_ENTITY["CODE"],
                },
                status=UNPROCESSIBLE_ENTITY["CODE"],
            )
        except Exception as error:
            logging.error(
                "Unexpected error occurred in auth middleware", exc_info=True)
            # return Response(
            #     {
            #         "message": "An unexpected error occurred",
            #         "status": "Error",
            #         "status_code": 500,
            #     },
            #     status=500,
            # )
            return JsonResponse(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    # "status_code": UN_AUTHORIZED["CODE"],
                },
                status=UN_AUTHORIZED["CODE"],
            )

    return wrapped_view


# leads middleware, but also admin will have access to all resources
def leads_auth_middleware(get_response):
    print("Leads Auth Middleware Initialized")

    def wrapped_view(request):
        try:
            if request.headers["Authorization"] and request.headers["X-CSRFToken"]:
                token = split_bearer_value(request.headers["Authorization"])
                decoded_token = decode_access_jwtoken(token)
                if decoded_token["isDecoded"]:
                    USER = UserModel.objects.filter(
                        user_id=decoded_token["payload"]
                    ).first()
                    if USER is not None:
                        if USER.role == "super-admin" or USER.role == "lead":
                            print("user authenticated")
                            return get_response(request, USER)
                        else:
                            return JsonResponse(
                                {
                                    "message": UN_AUTHORIZED["MESSAGE"],
                                    "status": UN_AUTHORIZED["STATUS"],
                                    # "status_code": UN_AUTHORIZED["CODE"],
                                },
                                status=UN_AUTHORIZED["CODE"],
                            )
                    #   un authenticated user
                    return JsonResponse(
                        {
                            "message": UN_AUTHORIZED["MESSAGE"],
                            "status": UN_AUTHORIZED["STATUS"],
                            # "status_code": UN_AUTHORIZED["CODE"],
                        },
                        status=UN_AUTHORIZED["CODE"],
                    )
                return JsonResponse(
                    {
                        "message": UN_AUTHORIZED["MESSAGE"],
                        "status": UN_AUTHORIZED["STATUS"],
                        # "status_code": UN_AUTHORIZED["CODE"],
                    },
                    status=UN_AUTHORIZED["CODE"],
                )
        except KeyError as error:
            logging.error("KeyError Occurred ", error)

            # return Response(
            #     {
            #         "message": UN_AUTHORIZED["MESSAGE"],
            #         "status": UN_AUTHORIZED["STATUS"],
            #         "status_code": UN_AUTHORIZED["CODE"],
            #     },
            #     status=401,
            # )

            return JsonResponse(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    # "status_code": UN_AUTHORIZED["CODE"],
                },
                status=UN_AUTHORIZED["CODE"],
            )

        except (
            django.http.request.RawPostDataException,
            json.decoder.JSONDecodeError,
        ) as error:
            logging.error("Unexpected error occurred in auth middleware")
            return JsonResponse(
                {
                    "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                    "status": UNPROCESSIBLE_ENTITY["STATUS"],
                    # "status_code": UNPROCESSIBLE_ENTITY["CODE"],
                },
                status=UNPROCESSIBLE_ENTITY["CODE"],
            )
        except Exception as error:
            logging.error(
                "Unexpected error occurred in auth middleware", exc_info=True)
            # return Response(
            #     {
            #         "message": "An unexpected error occurred",
            #         "status": "Error",
            #         "status_code": 500,
            #     },
            #     status=500,
            # )
            return JsonResponse(
                {
                    "message": UN_AUTHORIZED["MESSAGE"],
                    "status": UN_AUTHORIZED["STATUS"],
                    # "status_code": UN_AUTHORIZED["CODE"],
                },
                status=UN_AUTHORIZED["CODE"],
            )

    return wrapped_view
