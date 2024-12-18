from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password, check_password
from dotenv import load_dotenv
from uuid import uuid4
import json

# Modules
from api.models.company_model import CompanyModel
from api.serializers.company_serializer import CompanySerializer

# views in below here

@api_view(["POST"])
def register_company(request):
    print("api.views.company.register_company()")
    REQUEST_BODY = json.loads(request.body)
    # logic here

@api_view(["GET"])
def get_company(request):
    print("api.views.company.get_company()")
    
    REQUEST_BODY = json.loads(request.body)
    # do logic here