from os import stat
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.test.utils import override_settings
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from decouple import config

# getting user model
User = get_user_model()

@override_settings(EMAIL_BACKEND=config("EMAIL_BACKEND"))
class AuthenticationTests(APITestCase):
    def setUp(self):
        login_user_via_email_url = reverse("users:login_via_email")
        login_user_via_email_data = {
            "email": "online@example.com",
            "password": "superpowerfulpassword"
        } 
        self.logout_url = reverse("users:logout")
        self.user = User.objects.create_user(email="online@example.com", username="online", phone_number="09335008000", password="superpowerfulpassword")
        self.user2 = User.objects.create_user(email="online2@example.com", username="online2", phone_number="09335007000", password="superpowerfulpassword")
        self.login_user_via_email = self.client.post(login_user_via_email_url, login_user_via_email_data) 
        self.tokens_for_logout = self.login_user_via_email.json()
        self.reset_password_uidb64 = urlsafe_base64_encode(smart_bytes(self.user.pk))
        self.reset_password_token = PasswordResetTokenGenerator().make_token(self.user)

    def test_registeration(self):
        registeration_url = reverse("users:registeration")
        registeration_data = {
            "email": "user@example.com",
            "username": "user",
            "phone_number": "09122004000",
            "password": "superpowerfulpassword",
            "repeated_password": "superpowerfulpassword"
        }
        registeration_response = self.client.post(registeration_url, registeration_data)
        
        # testing part

        self.assertEqual(registeration_response.status_code, status.HTTP_201_CREATED)

    def test_login_via_email(self):
        login_via_email_url = reverse("users:login_via_email")
        login_via_email_data = {
            "email": "online@example.com",
            "password": "superpowerfulpassword"
        }
        login_via_email_response = self.client.post(login_via_email_url, login_via_email_data)

        # testing part

        self.assertEqual(login_via_email_response.status_code, status.HTTP_200_OK)

    def test_login_via_phone_number(self):
        login_via_phone_url = reverse("users:login_via_phoneNumber")
        login_via_phone_data = {
            "phone_number": "09335008000",
            "password": "superpowerfulpassword"
        }
        login_via_phone_response = self.client.post(login_via_phone_url, login_via_phone_data)

        # testing part

        self.assertEqual(login_via_phone_response.status_code, status.HTTP_200_OK)       

    def test_logout(self): 
        logout_data = {"refresh": self.tokens_for_logout["refresh"]}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.tokens_for_logout["access"]))
        logout_response = self.client.post(self.logout_url, logout_data)

        # testing part

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_with_bad_refresh_token(self):
        logout_data = {"refresh": "SuperTrashRefreshToken"}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.tokens_for_logout["access"]))
        logout_response = self.client.post(self.logout_url, logout_data)
        
        # testing part

        self.assertEqual(logout_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_with_already_blacklisted_refresh_token(self): 
        logout_data = {"refresh": self.tokens_for_logout["refresh"]}
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.tokens_for_logout["access"]))
        logout_response = self.client.post(self.logout_url, logout_data)
        logout_response_second_try = self.client.post(self.logout_url, logout_data)
        
        # testing part

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(logout_response_second_try.status_code, status.HTTP_400_BAD_REQUEST)

    def test_request_reset_password_link(self):
        request_reset_password_link_url = reverse("users:reset_password")
        request_reset_password_link_data = {"email": "online@example.com"}   
        request_rest_password_link_response = self.client.post(request_reset_password_link_url, request_reset_password_link_data)

        # testing part

        self.assertEqual(request_rest_password_link_response.status_code, status.HTTP_200_OK)

    def test_check_reset_password_link(self):
        check_reset_password_link_url = reverse("users:reset_password_confirm", kwargs={"uidb64": self.reset_password_uidb64, "token": self.reset_password_token})
        check_reset_password_link_response = self.client.get(check_reset_password_link_url) 

        # testing part

        self.assertEqual(check_reset_password_link_response.status_code, status.HTTP_202_ACCEPTED)      

    def test_set_new_password(self):
        set_new_password_url = reverse("users:reset_password_confirm")
        set_new_password_data = {"password": "superpassword", "repeated_password": "superpassword", "uidb64": self.reset_password_uidb64, "token": self.reset_password_token}
        set_new_password_response = self.client.patch(set_new_password_url, set_new_password_data)

        # testing part

        self.assertEqual(set_new_password_response.status_code, status.HTTP_200_OK)
