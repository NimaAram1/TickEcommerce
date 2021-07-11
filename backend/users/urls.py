from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("registeration", views.RegisterationApiView.as_view(), name="registeration"),
    path("login", views.LoginApiView.as_view(), name="login")
]