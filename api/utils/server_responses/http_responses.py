responses = {}

# SUCCESS RESPONSES
responses["SUCCESS"] = {
    "CODE": {"STANDARD": 200, "CREATED": 201, "ACCEPTED": 202, "NOCONTENT": 204},
    "STATUS": True,
}
# UNPROCESSIBLE ENTITY
responses["UNPROCESSIBLE_ENTITY"] = {
    "CODE": 422,
    "MESSAGE": "UNPROCESSABLE_ENTITY",
    "STATUS": False,
}

# SERVER ERROR
responses["SERVER_ERROR"] = {"CODE": 500, "MESSAGE": "DB_ERROR", "STATUS": False}

# UNAUTHORIZED USER
responses["UN_AUTHORIZED"] = {"CODE": 401, "MESSAGE": "NOT_AUTHORIZED", "STATUS": False}

# FORBIDEENACCESS
responses["FORBIDENACCESS"] = {
    "CODE": 403,
    "MESSAGE": "FORBIDEN_ACCESS",
    "STATUS": False,
}

SUCCESS = responses["SUCCESS"]
SUCCESS_CODE = SUCCESS["CODE"]

SERVER_ERROR = responses["SERVER_ERROR"]

UN_AUTHORIZED = responses["UN_AUTHORIZED"]

FORBIDEN_ACCESS = responses["FORBIDENACCESS"]

UNPROCESSIBLE_ENTITY = responses["UNPROCESSIBLE_ENTITY"]

# print(SUCCESS)
# print(responses)
