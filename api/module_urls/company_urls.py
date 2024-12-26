from django.urls import path, include
from api.views.company_views import get_company, register_company, update_company
from api.middleware.auth import admin_auth_middleware

urlpatterns = [
    path("get-company-by-id", admin_auth_middleware(get_company)),
    path("register-compan", admin_auth_middleware(register_company)),
    path("update-company", admin_auth_middleware(update_company)),
]
