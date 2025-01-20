from django.urls import path
from api.views.finances_views import create_customer

from api.middleware import auth_middleware

urlpatterns = [
    # stripe urls and views
    path("stripe/create-customer", auth_middleware(create_customer)),
    # stripe customer urls and views
    # path("user/")

]
