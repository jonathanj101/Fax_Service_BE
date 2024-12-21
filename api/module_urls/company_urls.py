from django.urls import path, include
from api.views.company_views import get_company, register_company, update_company

urlpatterns = [
    path("get-company-by-id/<str:id>", get_company),
    path("register-company", register_company),
    path("update-company/<str:id>", update_company),
]
