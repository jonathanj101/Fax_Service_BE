from django.urls import path, include
from api.middleware.auth import auth_middleware
from api.views.user_views import login, log_out, register, get_logged_in_user_info, forgot_password,reset_password,update_user


urlpatterns = [
    path("login", login),
    path("logout", log_out),
    path("register", register),
    path("get-logged-in-user-info", auth_middleware(get_logged_in_user_info)),
    path("forgot-password", forgot_password),
    path("reset-password", reset_password),
    path("update-user", auth_middleware(update_user)),
]
