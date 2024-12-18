from django.urls import path, include
from api.views.company_views import get_company

urlpatterns = [
    path("get-company", get_company)
]