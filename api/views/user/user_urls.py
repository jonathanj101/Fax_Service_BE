from django.urls import path, include
from .views import login, log_out, register, get_logged_in_user_info, forgot_password,reset_password,update_user


urlpatterns = [
    path('login',login),
    path("logout", log_out),
    path('register', register),
    path("get-logged-in-user-info", get_logged_in_user_info),
    path("forgot-password", forgot_password),
    path("reset-password", reset_password),
    path("update-user", update_user),

]
