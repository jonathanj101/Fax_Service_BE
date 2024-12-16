from django.urls import path, include

urlpatterns = [
    path('user/', include('api.views.user.user_urls'))
]