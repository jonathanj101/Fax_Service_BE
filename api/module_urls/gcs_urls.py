from django.urls import path, include
from api.views.gcs_views import (
    create_gcs_bucket,
    get_all_gcs_files,
    delete_gcs_files,
    upload_gcs_files,
    get_gcs_files
)
from api.middleware.auth import admin_auth_middleware

urlpatterns = [
    path("create-storage", admin_auth_middleware(create_gcs_bucket)),
    path("create-storage", admin_auth_middleware(create_gcs_bucket)),
    path("upload-files", admin_auth_middleware(upload_gcs_files)),
    path("delete-files", admin_auth_middleware(delete_gcs_files)),
    path("get-all-files", admin_auth_middleware(get_all_gcs_files)),
    path("get-file", admin_auth_middleware(get_gcs_files)),
]
