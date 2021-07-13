from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("registeration", views.RegisterationApiView.as_view(), name="registeration"),
    path("login-email", views.LoginViaEmailApiView.as_view(), name="loginViaEmail"),
    path("login-phone-number", views.LoginViaPhoneNumberApiView.as_view(), name="loginViaPhoneNumber"),
    path("logout", views.LogoutApiView.as_view(), name="logout")
]