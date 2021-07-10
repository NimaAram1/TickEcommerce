from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("registeration", views.RegisterationApiView.as_view(), name="registeration")
]