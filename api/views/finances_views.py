# contrib
import os
import json
import logging
import stripe


from django.views.decorators.csrf import ensure_csrf_cookie
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
import stripe.error

from api.utils.server_responses.http_responses import (
    SERVER_ERROR,
    SUCCESS,
    SUCCESS_CODE,
    UNPROCESSIBLE_ENTITY
)

# Loading environment variables
load_dotenv()

# Helpers

# Server responses

# Initialized stripe apy key
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]


@api_view(["POST"])
def create_customer(request, user_model):
    print("api.views.finances_views.create_customer()")

    try:
        # get request data
        DATA = json.loads(request.body)["data"]
        # separate user address data
        USER_ADDRESS = {
            "city": DATA["city"],
            "country": DATA["country"],
            "line1": DATA["addrsLine1"],
            "line2": DATA["addrsLine2"],
            "postal_code": DATA["postalCode"],
            "state": DATA["state"],
        }
        CARD_TOKEN = {
            "token": DATA["cardToken"]
        }
        
        # Stripe no longer sensible data, tokenization is preffered        
        # CARD_DATA = {
        #     "number": DATA["cardNum"],
        #     "cvc": DATA["cvc"],
        #     "exp_month": DATA["expMonth"],
        #     "exp_year": DATA["expYear"],
        # }
        try:
        #   create a payment method
            stripeCard = stripe.PaymentMethod.create(
                type="card",
                card=CARD_TOKEN
            )
        except stripe.error.CardError as error:
          print("An Stripe create payment method error occurred -> ",error)
          logging.error("An Stripe create payment method error occurred -> ",error)
          return Response(
                {
                    "message": f"{error.user_message}",
                    "status": SERVER_ERROR["STATUS"],
                },
                status=401
            )
        try:
            # create customer
            stripeCustomer = stripe.Customer.create(
                description="Testing API intent to create customer on Stripe",
                name= f"{user_model.first_name} {user_model.middle_name} {user_model.last_name}",
                email=f"{user_model.email}",
                payment_method=stripeCard['id'],
                invoice_settings={
                    "default_payment_method": stripeCard["id"]
                },
                phone=DATA["phoneNum"],
                address=USER_ADDRESS
            )
            
            # attach the customer stripe id to user model
            user_model.stripeID = stripeCustomer["id"]
            # save it (update user model)
            return Response({
                "message": "Success",
                "status":SUCCESS["STATUS"]
            },
            status=SUCCESS_CODE["STANDARD"]
                            
                            )
        except stripe.error.InvalidRequestError as error:
            print('Stripe invalid Request Error -> ', error.user_messsage)
            logging.error(f"An Invalid Request Occurred {error.user_message}")
            return Response(
                {
                    "message": error.user_message,
                    "status": SERVER_ERROR["STATUS"],
                },
                status=SERVER_ERROR["STATUS"]
            )

    except Exception as error:
        print("api.views.finances_views.create_customer() error ", error)
        logging.error("An Stripe create_customer error occurred ->", error)
        return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )


@api_view(["POST"])
def create_payment_method(request,user_model):
    print("api.views.finances_views.create_payment_method()")
    try:
        DATA = json.loads(request.body)["data"]
        # grab the payment method token from the request
        CARD_TOKEN = DATA["cardToken"]
        
        # attach the card token or payment method to the customer on Stripe
        try:
            stripeCustomer = stripe.PaymentMethod.attach(
                payment_method=CARD_TOKEN,
                customer=user_model.stripe_id
            )
            return Response({
                "message":"Success",
                "status": SUCCESS["STATUS"]
            },status=SUCCESS_CODE["STANDARD"])
        except (stripe.error.CardError,stripe.error.InvalidRequestError):
            print('An Stripe attach payment method error occurred -> ',error)
            logging.error('An Stripe attach payment method error occurred -> ',error)
            return Response({
                "message":f"{error.user_message}",
                "status":False
            },status=401)
    except Exception as error:
        print("An Error Occurred at create_payment_method()",error)
        logging.error("An Proccessing Request Error Occurred at create_payment_method()",error)
        return Response({
            "message":UNPROCESSIBLE_ENTITY["MESSAGE"],
            "status": UNPROCESSIBLE_ENTITY["STATUS"]
        },status=UNPROCESSIBLE_ENTITY["CODE"])
        
        
    except Exception as error:
      print("api.views.finances_views.create_payment_method() error -> ",error)
      logging.error("An Strpine create_paymethod error occurred -> ",error)
      return Response(
            {
                "message": SERVER_ERROR["MESSAGE"],
                "status": SERVER_ERROR["STATUS"],
            },
            status=SERVER_ERROR["CODE"],
        )
      
