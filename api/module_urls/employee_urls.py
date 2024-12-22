from django.urls import path, include
from api.views.employee_views import create_employee, get_employees_by_company_id

urlpatterns = [
    path("create-employee", create_employee),
    path("get-employees-by-company-id/<str:company_id>", get_employees_by_company_id),
]
