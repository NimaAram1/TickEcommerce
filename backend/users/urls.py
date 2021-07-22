from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("registeration", views.RegisterationApiView.as_view(), name="registeration"),
    path("login-email", views.LoginViaEmailApiView.as_view(), name="login_via_email"),
    path("login-phone-number", views.LoginViaPhoneNumberApiView.as_view(), name="login_via_phoneNumber"),
    path("logout", views.LogoutApiView.as_view(), name="logout"),
    path("reset-password", views.ResetPasswordApiView.as_view(), name="reset_password"),
    path("reset-password-confirm/<uidb64>/<token>", views.CheckPasswordTokenApiView.as_view(), name="reset_password_confirm"),
    path("reset-password-complete", views.SetNewPasswordApiView.as_view(), name="reset_password_confirm")
]