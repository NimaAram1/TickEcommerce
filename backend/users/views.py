from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    RegisterationSerializer,
    LoginSerializerViaEmail,
    LoginSerializerViaPhoneNumber,
    LogoutSerializer
)   

# getting user model
User = get_user_model()

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