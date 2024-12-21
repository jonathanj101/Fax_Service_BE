# contrib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv
from uuid import uuid4
import json

# Modules
from api.models.user_model import UserModel
from api.serializers.user_serializer import UserSerializer

# Helpers
from api.utils.helpers.helpers import generate_random_password, reset_password_notify_user, forgot_password_notify_user
from api.utils.server_responses.http_responses import SUCCESS, SUCCESS_CODE, SERVER_ERROR, UN_AUTHORIZED,FORBIDEN_ACCESS
# from api.utils.common.common import EMAIL_OWNER

# Auth
from api.utils.auth.jwt_auth import create_access_jwtoken,decode_access_jwtoken, create_refresh_jwtoken

# Loading environment variables
load_dotenv()

# unique id randominize
uid = uuid4()


@api_view(["OPTIONS", "PUT"])
def login(request):
    print("api.views.user.login")

    REQUEST_BODY = json.loads(request.body)

    USER_OBJ = {
        'username': REQUEST_BODY['username'],
        'password': REQUEST_BODY['password'],
    }
    # print(request.COOKIES.get("jwt-token"))
    USER_MODEL = UserModel.objects.filter(username=USER_OBJ["username"]).first()

    if USER_MODEL is not None and check_password(
        USER_OBJ["password"], USER_MODEL.password
    ):
        if check_password(USER_OBJ["password"], USER_MODEL.password):
            serializer = UserSerializer(UserModel.objects.filter(
                username=USER_OBJ["username"]), many=True).data

            secret_access = create_access_jwtoken(USER_MODEL.pk)
            secret_refresh = create_refresh_jwtoken(USER_MODEL.pk)

            serializer[0]["token"] = secret_access

            response = Response()
            response.set_cookie(key='secret_refresh', value=secret_refresh,
                                httponly=True, samesite="None")
            response.data = {
                "message": "You Log In successfully!",
                'data': serializer[0],
                "status_code": SUCCESS_CODE["STANDARD"],
                "status": SUCCESS["STATUS"],
            }

            return response
    else:
        return Response(
            {
                "message": f" The username/password  you entered, does not exis within our record! Please try again!",
                "status_code": UN_AUTHORIZED["CODE"],
                "status": UN_AUTHORIZED["STATUS"],
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

    return response


@api_view(['PUT', 'POST'])
def register(request):
    print("api.register()")

    REQUEST_BODY = json.loads(request.body)

    USER_OBJ = {
        "first_name": REQUEST_BODY['firstName'],
        "middle_name": REQUEST_BODY["middleName"],
        "last_name": REQUEST_BODY['lastName'],
        "email": REQUEST_BODY['email'],
        "username": REQUEST_BODY['username'],
        "password": make_password(REQUEST_BODY['password'], salt=None, hasher='default'),
        "role": REQUEST_BODY['role']
    }

    # FILTER USER BY USERNAME, TO CHECK IF SAME USERNAME EXISTS WITHIN DB
    FILTER_BY_USERNAME = UserModel.objects.filter(
        username=USER_OBJ['username']).first()

    # FILTER USER BY EMAIL, TO CHECK IF SAME EMAIL EXISTS WITHIN DB
    FILTER_BY_EMAIL = UserModel.objects.filter(email=USER_OBJ['email']).first()

    if FILTER_BY_USERNAME is not None:
        print("username is taken")
        return Response(
            {
                "message": f"{USER_OBJ['username']} is already taken. Please choose another username.",
                "status_code": SERVER_ERROR["CODE"],
                "status": SERVER_ERROR["STATUS"]
            }
        )

    elif FILTER_BY_EMAIL is not None:
        print("email is taken")
        return Response(
            {
                "message": f"{USER_OBJ['email']} is already taken. Please choose another email.",
                "status_code": SERVER_ERROR["CODE"],
                "status": SERVER_ERROR["STATUS"]
            }
        )

    elif FILTER_BY_EMAIL and FILTER_BY_USERNAME is not None:
        print("email and username are taken")
        return Response(
            {
                "message": f"username {USER_OBJ['username']} and e-mail {USER_OBJ['email']} are both taken. Please choose another username/email.",
                "status_code": SERVER_ERROR["CODE"],
                "status": SERVER_ERROR["STATUS"]
            }
        )

    else:
        print("saving user to db")
        # print(USER_OBJ)
        request.session["user"] = uid.int
        request.session.set_expiry(7500)
        USER = UserModel(first_name=USER_OBJ["first_name"], last_name=USER_OBJ["last_name"],
                    username=USER_OBJ["username"],middle_name=USER_OBJ['middle_name'], password=USER_OBJ["password"], email=USER_OBJ['email'], role=USER_OBJ["role"])
        USER.save()
        serializer = UserSerializer(UserModel.objects.filter(
            username=USER_OBJ["username"]), many=True).data
        # print(serializer)
        return Response(
            {
                "message": f"User {USER_OBJ['first_name']} {USER_OBJ['last_name']} has been created successfully!",
                'status_code': SUCCESS_CODE["CREATED"],
                'status': SUCCESS["STATUS"],
                "data": serializer
            }
        )

# need re-work logic with recently updated jwt auth logic
@api_view(["GET"])
def get_logged_in_user_info(request):
    print("api.get_logged_in_info()")

    REQUEST_BODY = json.loads(request.body)
    token = REQUEST_BODY["token"]

    try:
        isUser = decode_access_jwtoken(token)
        # user = User.objects.filter(pk=isUser).first()
        # if (user is not None):
        if isUser:
            print("found user")
            serializer = UserSerializer(
                UserModel.objects.filter(pk=isUser), many=True).data
            # USER_OBJ['first_name'] = user.first_name
            # USER_OBJ['last_name'] = user.last_name
            # USER_OBJ['email'] = user.email
            # USER_OBJ['role'] = user.role
            # USER_OBJ['bookings'] = user.bookings

            return Response(
                {
                    "status_code": SUCCESS_CODE["ACCEPTED"],
                    "status": SUCCESS["STATUS"],
                    "data": serializer[0]
                }
            )
    except jwt.exceptions.DecodeError as error:
        print("user not authenticated", error)
        return Response(
            {
                "message": f"{UN_AUTHORIZED['MESSAGE']}",
                "status_code": UN_AUTHORIZED["CODE"],
                "status": UN_AUTHORIZED["STATUS"],
            }
        )


@api_view(["POST"])
def forgot_password(request):
    print("api/forgot_password()")
    # get username from request body
    REQUEST_BODY = json.loads(request.body)
    # filter user model with that username
    # create session
    request.session["user"] = uid.int
    # set session expiration to 10 minutes only
    request.session.set_expiry(600)
    USER = UserModel.objects.filter(
        username=REQUEST_BODY['username']).first()
    if USER is not None:
        # We want to generate temporary password
        temporary_password = generate_random_password()
        # inside that email, there would be a link that would navigate user to a page to log in with that temporary password and then reset password.
        subject = "Company Name",
        subject2 = "Do-not reply to this email!"
        message = f"Forgot Password!"
        forgot_password_notify_user(
            subject, message, subject2, USER.email, USER.username)
        # send that temporary password to client side,
        # for user to able to proceed on reseting password on reset password page
        return Response(
            {
                "message": "RESET_PASSWORD",
                "status": True,
                "status_code": SUCCESS_CODE["STANDARD"],
                "data": temporary_password
            }
        )
    return Response(
        {
            "message": SERVER_ERROR["MESSAGE"],
            "status": SERVER_ERROR["STATUS"],
            "status_code": SERVER_ERROR["CODE"]
        }
    )


@api_view(["POST"])
def reset_password(request):
    print("api/reset_password()")
    REQUEST_BODY = json.loads(request.body)

    USERNAME = REQUEST_BODY["username"]
    NEW_PASSWORD = REQUEST_BODY["password"]

    # check if there is a user session if not then return an unauthorized access
    try:
        # request.session['user']

        USER = UserModel.objects.filter(username=USERNAME).first()
        if USER is not None:
            USER.password = make_password(
                NEW_PASSWORD, salt=None, hasher='default')
            # save new password
            USER.save()
            # send email to user for successfully resetting password
            subject = "Ideas GenteKaba Pro",
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
    except KeyError as error:
        print("api/reset_password, exception occurred -> ", error)
        return Response(
            {
                "message": UN_AUTHORIZED['MESSAGE'],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"]
            }
        )


@api_view(["POST"])
def update_user(request):
    print("api/update_user()")

    REQUEST_BODY = json.loads(request.body)
    DATA = REQUEST_BODY["data"]
    token = REQUEST_BODY["token"]
    try:
        isUser = decode_access_jwtoken(token)
        if isUser:
            USER = UserModel.objects.get(pk=isUser)
            serializer = UserSerializer(
                UserModel.objects.filter(pk=isUser), many=True).data
            if USER is not None:
                print("found user")
                for key, value in DATA.items():
                    # print(key, value)
                    setattr(USER, key, value)
                    USER.save()

                return Response(
                    {
                        "message": "SUCCESS",
                        "status": SUCCESS["STATUS"],
                        "status_code": SUCCESS_CODE["STANDARD"]
                    }
                )
            else:
                return Response(
                    {
                        "message": f"It seems username {serializer[0]['username']} does not exists!",
                        "status": SERVER_ERROR["MESSAGE"],
                        "status_code": SERVER_ERROR["CODE"]
                    }
                )
    except jwt.exceptions.DecodeError as error:
        print('api/update_user() User not authenticated! -> ', error)
        return Response(
            {
                "message": UN_AUTHORIZED["MESSAGE"],
                "status": UN_AUTHORIZED["STATUS"],
                "status_code": UN_AUTHORIZED["CODE"]
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
