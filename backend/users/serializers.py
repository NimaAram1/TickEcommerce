from django.utils.text import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers

# getting user model
User = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, help_text=_("Enter a valid password"))
    repeated_password = serializers.CharField(write_only=True, required=True, help_text=_("Enter your password again"))
    
    
    class Meta:
        model = User
        fields = ["email", "username", "phone_number", "password", "repeated_password"]

    
    def validate(self, data):
        if data["password"] and data["repeated_password"] and data["password"] != data["repeated_password"]:
            raise serializers.ValidationError(_("Password and repeated password must be the same"))
        return data

class LoginSerializerViaEmail(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, max_length=220, min_length=6, help_text=_("Enter your email"))
    password = serializers.CharField(write_only=True, required=True, help_text=_("Enter your password")) 
    class Meta:
        model = User
        fields = ["email", "password"]

    
    def validate(self, data):
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
    
        if not user:
            raise AuthenticationFailed(_("Your email or your password is incorrect"))

        elif not user.is_active:
            raise AuthenticationFailed(_("Your account has been disabled"))

        return super().validate(data) 

class LoginSerializerViaPhoneNumber(serializers.ModelSerializer):
    phone_number_regex = RegexValidator(regex=r"^09(1[0-9]|2[0-9]|3[0-9])[0-9]{3}[0-9]{4}$") 
    phone_number = serializers.CharField(write_only=True, required=True, validators=[phone_number_regex], help_text=_("Enter your phone number, Be care that your phone number must start with 091"))
    password = serializers.CharField(write_only=True, required=True, help_text=_("Enter your password"))
    
    
    class Meta:
        model = User
        fields = ["phone_number", "password"]
    
    
    def validate(self, data):
        phone_number = data["phone_number"]
        password = data["password"]
        user_instance = User.objects.get(phone_number=phone_number)
        user = authenticate(email=user_instance.email, password=password)
        
        if not user:
            raise AuthenticationFailed(_("Your email or your password is incorrect"))

        elif not user.is_active:
            raise AuthenticationFailed(_("Your account has been disabled"))

        return super().validate(data)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True, required=True, help_text=_("Enter your refresh key for logout"))
    
    default_error_messages = {
        "bad token": _("Your token doesn't valid")
    }
    
    
    def validate(self, data):
        self.token = data["refresh"]
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist() 
        except TokenError:
            self.fail("bad token")

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True, help_text=_("Enter your account's email"))

    class Meta:
        fields = ["email"]  

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=30, write_only=True, required=True, help_text=_("Please enter a powerful and unpredictable password"))
    repeated_password = serializers.CharField(min_length=6, max_length=30, write_only=True, required=True, help_text=_("Please re-enter your password again"))
    token = serializers.CharField(min_length=1, write_only=True, required=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True, required=True)

    class Meta:
        fields = ["password", "repeated_password", "token", "uidb64"]

    def validate(self, data):
        try:
            password = data["password"]
            repeated_password = data["repeated_password"]
            token = data["token"]
            uidb64 = data["uidb64"]
            if password == repeated_password:
                user_id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=user_id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed(_("The reset link is invalid"), 402)

                user.set_password(password)
                user.save()

                return (user) 
            else:
                raise AuthenticationFailed(_("Your passwords did not match"))       
        except:
            raise AuthenticationFailed(_("The reset link is invalid"), 403)
        
        return super().validate(data)             