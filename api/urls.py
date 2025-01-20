from django.urls import path, include

urlpatterns = [
    path("user/", include("api.module_urls.user_urls")),
    path("company/", include("api.module_urls.company_urls")),
    path("employees/", include("api.module_urls.employee_urls")),
    path("files/", include("api.module_urls.gcs_urls")),
    path("fax-services/", include("api.module_urls.fax_services_urls")),
    path("finance/", include("api.module_urls.finances_urls"))
]
