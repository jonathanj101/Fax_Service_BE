from django.urls import path, include

urlpatterns = [
    path("user/", include("api.module_urls.user_urls")),
    path("company/", include("api.module_urls.company_urls")),
    path("employees/", include("api.module_urls.employee_urls")),
]
