# contrib
from rest_framework.decorators import api_view
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv
import uuid
import json
import logging

# Modules
from api.models.user_model import UserModel
from api.serializers.user_serializer import UserSerializer

# Helpers
from api.utils.helpers.helpers import (
    generate_random_password,
    reset_password_notify_user,
    forgot_password_notify_user,
    split_bearer_value,
)
from api.utils.server_responses.http_responses import (
    SUCCESS,
    SUCCESS_CODE,
    SERVER_ERROR,
    UN_AUTHORIZED,
    FORBIDEN_ACCESS,
    UNPROCESSIBLE_ENTITY,
)

# from api.utils.common.common import EMAIL_OWNER

# Auth
from api.utils.auth.jwt_auth import create_access_jwtoken,decode_access_jwtoken, create_refresh_jwtoken

# Loading environment variables
load_dotenv()


@api_view(["OPTIONS", "PUT"])
@ensure_csrf_cookie
def login(request):
    print("api.views.user.login")

    REQUEST_BODY = json.loads(request.body)

    try:
        USER_OBJ = {
            "username": REQUEST_BODY["username"],
            "password": REQUEST_BODY["password"],
        }
        # print(request.COOKIES.get("jwt-token"))
        USER_MODEL = UserModel.objects.filter(username=USER_OBJ["username"]).first()

        if USER_MODEL is not None and check_password(
            USER_OBJ["password"], USER_MODEL.password
        ):
            if check_password(USER_OBJ["password"], USER_MODEL.password):
                serializer = UserSerializer(
                    UserModel.objects.filter(username=USER_OBJ["username"]), many=True
                ).data[0]

                secret_access = create_access_jwtoken(serializer["user_id"])["payload"]
                secret_refresh = create_refresh_jwtoken(serializer["user_id"])[
                    "payload"
                ]

                response = Response()
                # response.set_cookie(
                #     key="secret_refresh",
                #     value=secret_refresh,
                #     httponly=True,
                #      samesite="None",
                # )
                # response.set_cookie("csrftoken", secret_refresh)
                response.data = {
                    "message": "You Log In successfully!",
                    "data": serializer,
                    "status_code": SUCCESS_CODE["STANDARD"],
                    "status": SUCCESS["STATUS"],
                }

                response.headers = {
                    "Authorization": secret_access,
                    # "X-CSRFToken": secret_refresh,
                }
                print(response)
                # print(response.COOKIES)

                return response
        else:
            return Response(
                {
                    "message": f" The username/password  you entered, does not exis within our record! Please try again!",
                    "status_code": SUCCESS["CODE"]["STANDARD"],
                    "status": SUCCESS["STATUS"],
                }
            )
    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

    except (AssertionError, AttributeError) as error:
        print("An AssertionError or AttributeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

@api_view(["PUT"])
def log_out(request):
    print("api.views.user.log_out()")
    # print(request.COOKIES)
    response = Response()
    response.delete_cookie(key="secret_refresh", samesite="None")
    response.data = {
        "message": "You successfully logged out!",
        "status_code": SUCCESS_CODE["STANDARD"],
        "status": SUCCESS["STATUS"]
    }

    response.headers["Authorization"] = ""

    return response

@api_view(['PUT', 'POST'])
def register(request):
    print("api.register()")

    REQUEST_BODY = json.loads(request.body)

    try:
        USER_OBJ = {
            "first_name": REQUEST_BODY["firstName"],
            "middle_name": REQUEST_BODY["middleName"],
            "last_name": REQUEST_BODY["lastName"],
            "email": REQUEST_BODY["email"],
            "username": REQUEST_BODY["username"],
            "password": make_password(
                REQUEST_BODY["password"], salt=None, hasher="default"
            ),
            "role": REQUEST_BODY["role"],
        }

        # FILTER USER BY USERNAME, TO CHECK IF SAME USERNAME EXISTS WITHIN DB
        FILTER_BY_USERNAME = UserModel.objects.filter(
            username=USER_OBJ["username"]
        ).first()

        # FILTER USER BY EMAIL, TO CHECK IF SAME EMAIL EXISTS WITHIN DB
        FILTER_BY_EMAIL = UserModel.objects.filter(email=USER_OBJ["email"]).first()

        if FILTER_BY_USERNAME is not None:
            print("username is taken")
            return Response(
                {
                    "message": f"{USER_OBJ['username']} is already taken. Please choose another username.",
                    "status_code": SERVER_ERROR["CODE"],
                    "status": SERVER_ERROR["STATUS"],
                }
            )

        elif FILTER_BY_EMAIL is not None:
            print("email is taken")
            return Response(
                {
                    "message": f"{USER_OBJ['email']} is already taken. Please choose another email.",
                    "status_code": SERVER_ERROR["CODE"],
                    "status": SERVER_ERROR["STATUS"],
                }
            )

        elif FILTER_BY_EMAIL and FILTER_BY_USERNAME is not None:
            print("email and username are taken")
            return Response(
                {
                    "message": f"username {USER_OBJ['username']} and e-mail {USER_OBJ['email']} are both taken. Please choose another username/email.",
                    "status_code": SERVER_ERROR["CODE"],
                    "status": SERVER_ERROR["STATUS"],
                }
            )

        else:
            print("saving user to db")
            # print(USER_OBJ)
            # request.session["user"] = uid.int
            # request.session.set_expiry(7500)
            USER = UserModel(
                first_name=USER_OBJ["first_name"],
                last_name=USER_OBJ["last_name"],
                username=USER_OBJ["username"],
                middle_name=USER_OBJ["middle_name"],
                password=USER_OBJ["password"],
                email=USER_OBJ["email"],
                role=USER_OBJ["role"],
            )
            USER.save()
            serializer = UserSerializer(
                UserModel.objects.filter(username=USER_OBJ["username"]), many=True
            ).data[0]
            # print(serializer)
            return Response(
                {
                    "message": f"User {USER_OBJ['first_name']} {USER_OBJ['last_name']} has been created successfully!",
                    "status_code": SUCCESS_CODE["CREATED"],
                    "status": SUCCESS["STATUS"],
                    "data": serializer,
                }
            )

    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

    except AssertionError as error:
        print("An AssertionError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )


# need re-work logic with recently updated jwt auth logic
@api_view(["GET"])
def get_logged_in_user_info(request, user_model):  # data = user model from middleware
    print("api.get_logged_in_info()")
    try:
        serializer = UserSerializer(
            UserModel.objects.filter(user_id=user_model.user_id), many=True
        ).data[0]

        return Response(
            {
                "status_code": SUCCESS_CODE["ACCEPTED"],
                "status": SUCCESS["STATUS"],
                "data": serializer,
            }
        )
    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

    except (AssertionError, AttributeError) as error:
        print("An AssertionError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )


@api_view(["POST"])
def forgot_password(request):
    print("api/forgot_password()")
    # get username from request body
    REQUEST_BODY = json.loads(request.body)
    try:
        USER = UserModel.objects.filter(username=REQUEST_BODY["username"]).first()
        if USER is not None:
            # We want to generate temporary password
            temporary_password = generate_random_password()
            # inside that email, there would be a link that would navigate user to a page to log in with that temporary password and then reset password.
            subject = ("Company Name",)
            subject2 = "Do-not reply to this email!"
            message = f"Forgot Password!"
            forgot_password_notify_user(
                subject, message, subject2, USER.email, USER.username
            )
            # send that temporary password to client side,
            # for user to able to proceed on reseting password on reset password page
            return Response(
                {
                    "message": "RESET_PASSWORD",
                    "status": True,
                    "status_code": SUCCESS_CODE["STANDARD"],
                    "data": temporary_password,
                }
            )
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
                "status_code": SERVER_ERROR["CODE"],
            }
        )
    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("An KeyError or TypeError Occurred -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

    except AssertionError as error:
        print("An AssertionError Occurred -> ", error)
        logging.error("An AssertionError Occurred -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

@api_view(["POST"])
def reset_password(request):
    print("api/reset_password()")
    REQUEST_BODY = json.loads(request.body)

    try:
        # request.session['user']

        USERNAME = REQUEST_BODY["username"]
        NEW_PASSWORD = REQUEST_BODY["password"]
        USER = UserModel.objects.filter(username=USERNAME).first()
        if USER is not None:
            USER.password = make_password(
                NEW_PASSWORD, salt=None, hasher='default')
            # save new password
            USER.save()
            # send email to user for successfully resetting password
            subject = ("Fax Service System Inc",)
            subject2 = "Do-not reply to this email!"
            message = "Password reset successfully!"
            reset_password_notify_user(
                subject, subject2, message, USER.email, USER.username)
            return Response(
                {
                    "message": "SUCCESS",
                    "status": SUCCESS["STATUS"],
                    "status_code": SUCCESS_CODE["STANDARD"],
                }
            )
        return Response(
            {
                "message": f"{USERNAME} is not found!",
                "status": SERVER_ERROR["STATUS"],
                "status_code": SERVER_ERROR["CODE"]
            }
        )
    except (KeyError, TypeError, ValueError, AttributeError) as error:
        print("api/reset_password, exception occurred -> ", error)
        logging.error("An KeyrError, TypeError, ValueError", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )


@api_view(["POST"])
@ensure_csrf_cookie
def update_user(request, user_model):
    print("api/update_user()")
    try:
        REQUEST_BODY = json.loads(request.body)
        DATA = REQUEST_BODY["data"]
        user_id = DATA["user_id"]
        update_data = DATA["update_data"]

        USER = UserModel.objects.get(user_id=DATA["user_id"])
        if USER is not None:

            print("found user")
            for key, value in update_data.items():
                # print(key, value)
                setattr(USER, key, value)
                USER.save()
            serializer = UserSerializer(
                UserModel.objects.filter(user_id=user_model.user_id), many=True
            ).data[0]
            return Response(
                {
                    "message": "SUCCESS",
                    "status": SUCCESS["STATUS"],
                    "status_code": SUCCESS_CODE["STANDARD"],
                }
            )
        return Response(
            {
                "message": f"It seems that user does not exists within our database!",
                "status": SERVER_ERROR["STATUS"],
                "status_code": SERVER_ERROR["CODE"],
            }
        )
    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

    except (AssertionError, ValueError, AttributeError) as error:
        print("An AssertionError or ValueError, AttributeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )


@api_view(["GET"])
@ensure_csrf_cookie
def get_user_by_email(request, user_model):
    print("api.views.user_view.get_user_by_email()")
    try:
        REQUEST_BODY = json.loads(request.body)
        DATA = REQUEST_BODY["data"]

        USER = UserModel.objects.get(email=DATA["email"])
        if USER is not None:
            serializer = UserSerializer(
                UserModel.objects.filter(email=USER.email), many=True
            ).data[0]
            return Response(
                {
                    "message": "SUCCESS",
                    "data": serializer,
                    "status": SUCCESS["STATUS"],
                    "status_code": SUCCESS_CODE["STANDARD"],
                }
            )
        return Response(
            {
                "message": f"It seems that user does not exists within our database!",
                "status": SERVER_ERROR["STATUS"],
                "status_code": SERVER_ERROR["CODE"],
            }
        )
    except (KeyError, TypeError) as error:
        print("An KeyError or TypeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UNPROCESSIBLE_ENTITY["MESSAGE"],
                "status": UNPROCESSIBLE_ENTITY["STATUS"],
                "status_code": UNPROCESSIBLE_ENTITY["CODE"],
            }
        )

    except (AssertionError, ValueError, AttributeError) as error:
        print("An AssertionError or ValueError, AttributeError Occurred -> ", error)
        logging.error("logging error -> ", error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"],
            }
        )


# would need to brainstorm this approach
# @api_view(["POST"])
# def upload_image(request):

#     # request_body = json.loads(request.data)
#     request_body = request.data
#     # print(json.loads(request.file))

#     print(request_body)
#     promotions = Promotions.objects.all()

#     # promoton = Promotions(
#     #     promotion_id=request_body['id'], name=request_body["name"], price=2553.99, active=True, main_photo=request_body['file'])

#     # promoton.save()

#     # data = promoton

#     return Response(
#         {
#             "message": "ok",
#             "data": "serializer"
#         }
#     )


# @api_view(["GET"])
# def get_all_promotions(request):

#     serializer = PromotionsSerializer(Promotions.objects.all(), many=True).data
#     print(serializer)

#     return Response(
#         {
#             "data": serializer
#         }
#     )
