import jwt
import datetime

def create_access_jwtoken(user_id):
    print("api/utils/auth/jwt_auth.create_access_jwtoken")
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow(),
    }
    try:
        token = jwt.encode(payload, 'secret_access', algorithm='HS256')
    except jwt.exceptions.PyJWKError as error:
        print(token)
        print("api/helpers/auth/jwt_auth.create_access_jwtoken error -> ", error)
        return {"isToken": False, "error": error}
    return {"isToken": True, "token": token}


def decode_access_jwtoken(token):
    print("api/helpers/auth/jwt_auth.decode_access_jwtoken")
    try:
        payload = jwt.decode(token, 'secret_access', algorithms="HS256")
        return {"isToken": True, "data": payload["user_id"]}
    except KeyError as error:
        print("api/helpers/auth/jwt_auth.decode_access_jwtoken error -> ", error)
        return {"isToken": False, "error": error}
    except jwt.exceptions.DecodeError as error:
        print("api/helpers/auth/jwt_auth.decode_access_jwtoken error -> ", error)
        return {"isToken": False, "error": error}
    except jwt.exceptions.ExpiredSignatureError as error:
        print("api/helpers/auth/jwt_auth.decode_access_jwtoken error -> ", error)
        return {"isToken": False, "error": error}


def create_refresh_jwtoken(user_id):
    print("api/helpers/auth/jwt_auth.create_refresh_jwtoken")
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow(),
    }

    try:

        token = jwt.encode(payload, 'secret_refresh', algorithm='HS256')
    except KeyError as error:
        print('jwt_auth.create_refresh_jwToken() error -> ', error)
        return {"isToken": False, "error": error}

    return {"isToken": True, "token": token}


def decode_refresh_jwtoken(token):
    print("api/helpers/auth/jwt_auth.decode_refresh_jwtoken")
    try:
        payload = jwt.decode(token, "secret_access", algorithms="H5256")
    except KeyError as error:
        print("api/helpers/auth/jwt_auth.decode_refresh_jwtoken error -> ", error)
        return {"isToken": False, "error": error}
    except jwt.exceptions.DecodeError as error:
        print("api/helpers/auth/jwt_auth.decode_refresh_jwtoken error -> ", error)
        return {"isToken": False, "error": error}
    except jwt.exceptions.ExpiredSignatureError as error:
        print("api/helpers/auth/jwt_auth.decode_refresh_jwtoken error -> ", error)
        return {"isToken": False, "error": error}

    return {"isToken": True, "data": +payload["user_id"]}
