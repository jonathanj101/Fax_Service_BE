import os
# contrib
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse
from dotenv import load_dotenv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

import json
import logging
import requests
import base64


# Modules
#  fax models

# Helpers
from api.utils.helpers.helpers import generate_fax_confirmation

from api.utils.server_responses.http_responses import (
    SUCCESS,
    SERVER_ERROR,

)

load_dotenv()

FAX_API_URL = f"https://{os.environ["FAX_SPACE_NAME"]
                         }.signalwire.com/api/laml/2010-04-01/Accounts/{os.environ['PROJECT_ID']}/Faxes"
API_CREDENTIALS = f"{os.environ["PROJECT_ID"]}:{os.environ["FAX_API_TOKEN"]}"
ENCODED_CREDS = base64.b64encode(API_CREDENTIALS.encode()).decode()


@api_view(["GET"])
def generate_pdf_reportlab(request):
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="confirmation.pdf"'

    COMPANY_DATA = {
        "company_name": json.loads(request.body)["companyName"],
        "company_address": json.loads(request.body)["companyAddress"],
        "company_phone_number": json.loads(request.body)["companyPhoneNum"],
        "company_fax_number": json.loads(request.body)["companyFaxNum"],
        "sender": json.loads(request.body)["sender"],
        "total_pages": json.loads(request.body)["totalPages"],
    }

    FAX_DATA = {
        "fax_sent_time": json.loads(request.body)["faxSentTime"],
        "confirmation_id": json.loads(request.body)["confirmationId"],
        "recipient": json.loads(request.body)["recipient"],
        "pages_delivered": json.loads(request.body)["pagesDelivered"],
        "fax_status": json.loads(request.body)["faxStatus"],
        "fax_delivered": json.loads(request.body)["faxDeliveredTime"],
    }

    # Create a canvas object
    buffer = response
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    confirmation = generate_fax_confirmation(
        pdf_canvas, COMPANY_DATA, FAX_DATA)

    return response


@api_view(["GET"])
def get_all_faxes(request):
    print("api.views.fax_services_views.get_all_faxes()")

    headers = {
        'Accept': 'application/json',
        # 'Authorization': f"Basic {ENCODED_CREDS}"
    }

    try:
        # print(x)
        response = requests.get(url=FAX_API_URL,
                                params="", headers=headers, data={})
        # print(response.json())
        if response.status_code >= 200 and response.status_code <= 204:

            return Response({
                "message": "tesitng",
                "data": response.json(),
                "status": SUCCESS["STATUS"]
            },
                status=201
            )
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])
    except Exception as error:
        print('An exception occurred', error)
        return Response(
            {
                "message": "An Error Occured While Retriving Faxes. Please Try Again Later!",
                "status": SERVER_ERROR["STATUS"]
            },
            status=SERVER_ERROR["CODE"]
        )


@api_view(["POST"])
def send_fax(request):
    print("api.views.fax_services_views.send_fax()")
    try:
        REQUEST_BODY = json.loads(request.body)["data"]

        payload = {
            "MediaUrl": REQUEST_BODY["mediaUrl"],
            "To": REQUEST_BODY["recipient"],
            "From": REQUEST_BODY["sender"],
            # "Quality": "standard" # default value standard, option = fine or superfine
            # StatusCallback: api endpoint to send a POST request when the status of a fax changes.
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'Authorization': f"Basic {ENCODED_CREDS}"
        }

        response = requests.post(
            url=FAX_API_URL, data=payload, headers=headers)

        print(response)
        if response.status_code >= 200 and response.status_code <= 204:

            return Response({
                "message": "tesitng",
                "data": response.json(),
                "status": SUCCESS["STATUS"]
            },
                status=201
            )
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])

    except Exception as error:
        print("Fax Services Error Occured send_fax() ->", error)
        logging.error("Fax Services Error Occured send_fax() ->", error)
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])


@api_view(["POST"])
def delete_fax_by_id(request):
    print("api.views.fax_services_views.delete_fax_by_id()")
    try:
        REQUESt_BODY = json.loads(request.body)["data"]
        DELETE_FAX_URL = f"{FAX_API_URL}/{REQUESt_BODY['faxId']}"
        payload = {}

        headers = {
            "Authorization": f"Basic {ENCODED_CREDS}"
        }

        response = requests.delete(
            url=DELETE_FAX_URL, headers=headers, data=payload)

        print(response)

        if response.status_code >= 200 and response.status_code <= 204:
            return Response({
                "message": "Deleted fax successully!",
                "status": SUCCESS["STATUS"]
            },
                status=201
            )
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])

    except Exception as error:
        print("Fax Services Error Occured delete_fax_by_id() ->", error)
        logging.error(
            "Fax Services Error Occured delete_fax_by_id() ->", error)
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])


@api_view(["POST"])
def update_fax_by_id(request):
    print("api.views.fax_services_views.update_fax_bY_id()")

    try:
        REQUESt_BODY = json.loads(request.body)["data"]
        DELETE_FAX_URL = f"{FAX_API_URL}/{REQUESt_BODY['faxId']}"
        payload = {}

        headers = {
            "Authorization": f"Basic {ENCODED_CREDS}"
        }

        response = requests.delete(
            DELETE_FAX_URL, headers=headers, data=payload)

        print(response)

        if response.status_code >= 200 and response.status_code <= 204:
            return Response({
                "message": "tesitng",
                "data": response.json(),
                "status": SUCCESS["STATUS"]
            },
                status=201
            )
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])

    except Exception as error:
        print("Fax Services Error Occured update_fax_by_id() ->", error)
        logging.error("Fax Services Error Occured update_fax_by_id ->", error)
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])


@api_view(["GET"])
def get_fax_by_id(request):
    print("api.views.fax_services_views.get_fax_by_id()")

    try:
        REQUESt_BODY = json.loads(request.body)["data"]
        GET_FAX_URL = f"{FAX_API_URL}/{REQUESt_BODY['faxId']}"
        payload = {}

        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {ENCODED_CREDS}"
        }

        response = requests.get(
            url=GET_FAX_URL, headers=headers, data=payload)

        print(response)

        if response.status_code >= 200 and response.status_code <= 204:
            return Response({
                "message": "tesitng",
                "data": response.json(),
                "status": SUCCESS["STATUS"]
            },
                status=201
            )
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])

    except Exception as error:
        print("Fax Services Error Occured update_fax_by_id() ->", error)
        logging.error("Fax Services Error Occured update_fax_by_id ->", error)
        return Response({
            "message": "There seems an error occurred on our end! Please try again later!",
            "statis": SERVER_ERROR["STATUS"]
        },
            status=SERVER_ERROR["CODE"])
