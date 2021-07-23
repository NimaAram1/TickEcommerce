from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RegisterationSerializer,
    LoginSerializerViaEmail,
    LoginSerializerViaPhoneNumber,
    LogoutSerializer,
    ResetPasswordSerializer,
    SetNewPasswordSerializer
) 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.reverse import reverse
from .utils import Tools

# getting user model
User = get_user_model()

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = ['http', 'https']

class RegisterationApiView(APIView):
    """
    Get username, email, phone number, and password from the user
    and save it in the database
    """
    def post(self, request):
        if request.user.is_anonymous:
            data = RegisterationSerializer(data=request.data)
            if data.is_valid():
                User.objects.create_user(email=data.validated_data["email"], username=data.validated_data["username"],
                password=data.validated_data["password"], phone_number=data.validated_data["phone_number"])
                
                return Response({
                "message": f'{data.validated_data["email"]} account created successfully'
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "message": "You already authorized"
            }, status=status.HTTP_400_BAD_REQUEST)            

class LoginViaEmailApiView(GenericAPIView):
    """
    Get email and password and authenticate user with those, Then
    generate access and refresh token for user 
    """

    serializer_class = LoginSerializerViaEmail

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = authenticate(email=email, password=password)
        tokens = RefreshToken.for_user(user)

        return Response({
            "access": str(tokens.access_token),
            "refresh": str(tokens)
        }, status=status.HTTP_200_OK)

class LoginViaPhoneNumberApiView(GenericAPIView):
    """
    Get phone number and password and authenticate user with those, Then
    generate access and refresh token for user 
    """

    serializer_class = LoginSerializerViaPhoneNumber

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        phone_number = serializer.validated_data["phone_number"]
        password = serializer.validated_data["password"]
        user_instance = User.objects.get(phone_number=phone_number)
        user = authenticate(email=user_instance.email, password=password)
        tokens = RefreshToken.for_user(user)

        return Response({
            "access": str(tokens.access_token),
            "refresh": str(tokens)
        }, status=status.HTTP_200_OK)

class LogoutApiView(GenericAPIView):
    """
    Get refresh token from the user(without user knows) and blacklist his key
    for logout  
    """

    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class ResetPasswordApiView(APIView):
    """
    Get account's email from user and send a reset password link
    for user's email
    """
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data["email"]
    
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=request).domain
                relative_link = reverse("users:reset_password_confirm", kwargs={"uidb64": uidb64, "token": token})
                absurl = "http://" + current_site + relative_link 
                email_body = _("Dear ") + user.username + _(", \nUse link below to reset your password \n") + absurl
                email_context = {"email_body": email_body, "to_email": [user.email], "email_subject": _("Reset your password")}
            
                Tools.send_email(email_context)

                return Response({
                    "success": _("We have sent you a link that you can reset your password with it")
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": _("Your email did not exist in our records")
                })     
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)       

class CheckPasswordTokenApiView(GenericAPIView):
    """
    Open reset link and check that; If it is valid
    user can changes the password
    """
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if PasswordResetTokenGenerator().check_token(user, token) == True:
                return Response({
                    "message": _("Reset password link is valid")
                },  status=status.HTTP_202_ACCEPTED)
                
                # Also you can use CustomRedirect here instead of sending a response if you
                # want to have a redirect here(based on your needs).
            
            else:
                return Response({
                   "error": _("Token is not valid, Please request new one.")  
                },  status=status.HTTP_400_BAD_REQUEST) 

        except DjangoUnicodeDecodeError as error:
            return Response({
                "error": _("Token is not valid, Please request new one.")
            },  status=status.HTTP_400_BAD_REQUEST)          

class SetNewPasswordApiView(GenericAPIView):
    """
    Get password, repeated_password, token, and uidb64
    and reset user's password
    """

    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "success": _("Password reset success")
        }, status=status.HTTP_200_OK)                    