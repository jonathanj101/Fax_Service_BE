from django.urls import path
from api.views.fax_services_views import generate_pdf_reportlab, get_all_faxes, send_fax, delete_fax_by_id, get_fax_by_id

#  Middleware
from api.middleware.auth import auth_middleware

urlpatterns = [
    path("generate-fax", auth_middleware(generate_pdf_reportlab)),
    path("list-all-fax", auth_middleware(get_all_faxes)),
    path("send-fax", auth_middleware(send_fax)),
    path("get-fax-by-id", auth_middleware(get_fax_by_id)),
    path("delete-fax-by-id", auth_middleware(delete_fax_by_id))
]
