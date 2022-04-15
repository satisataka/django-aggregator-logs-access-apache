from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import SignUpView, MainLoginView

app_name = "main"

urlpatterns = [

    path("register/", SignUpView.as_view(), name="register"),
    path("login/", MainLoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name= "logout"),
]
