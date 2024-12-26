from django.urls import path, include
from api.views.employee_views import (
    create_employee,
    get_employees_by_company_id,
    update_employee_status,
    # get_employee_by_company_id,
)
from api.middleware.auth import admin_auth_middleware, auth_middleware

urlpatterns = [
    path("create-employee", admin_auth_middleware(create_employee)),
    path(
        "get-employees-by-company-id",
        admin_auth_middleware(get_employees_by_company_id),
    ),
    path(
        "update-employee",
        admin_auth_middleware(update_employee_status),
    ),
    # path("get-employee/<str:company_id>", get_employee_by_company_id),
]
