from django.urls import path, include
from api.views.gcs_views import (
    create_gcs_bucket,
    get_all_files,
    delete_files,
    upload_files,
    get_file,
)

from api.middleware.auth import admin_auth_middleware

urlpatterns = [
    path("create-storage", admin_auth_middleware(create_gcs_bucket)),
    path("delete-files", admin_auth_middleware(delete_files)),
    path("upload-files", admin_auth_middleware(upload_files)),
    path("get-all-files", admin_auth_middleware(get_all_files)),
    path("get-file", admin_auth_middleware(get_file)),
]
