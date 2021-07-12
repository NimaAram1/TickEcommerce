from rest_framework import fields, serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework.exceptions import AuthenticationFailed

# getting user model
User = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, help_text='یک رمز عبور امن وارد نمایید')
    repeated_password = serializers.CharField(write_only=True, required=True, help_text="تایید رمز عبور خود را وارد نمایید")
    class Meta:
        model = User
        fields = ["email", "username", "phone_number", "password", "repeated_password"]

    def validate(self, data):
        if data["password"] and data["repeated_password"] and data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("رمز عبور و تایید آن باید یکی باشد")
        return data

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(RegisterationSerializer, self).create(validated_data) 

class LoginSerializerViaEmail(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, max_length=220, min_length=6, help_text="ایمیل خود را وارد نمایید")
    password = serializers.CharField(write_only=True, required=True, help_text='رمز عبور خود را وارد نمایید') 
    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, data):
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
        
        if not user:
            raise AuthenticationFailed("رمز عبور یا ایمیل شما صحیح نمی باشد.")

        elif not user.is_active:
            raise AuthenticationFailed("اکانت شما غیر فعال شده است")

        return super().validate(data) 

class LoginSerializerViaPhoneNumber(serializers.ModelSerializer):
    phone_number_regex = RegexValidator(regex=r"^09(1[0-9]|2[0-9]|3[0-9])[0-9]{3}[0-9]{4}$") 
    phone_number = serializers.CharField(write_only=True, required=True, validators=[phone_number_regex], help_text="شماره موبایل خود را بهمراه صفر اول آن وارد کنید")
    password = serializers.CharField(write_only=True, required=True, help_text='رمز عبور خود را وارد نمایید')
    class Meta:
        model = User
        fields = ["phone_number", "password"]
    
    def validate(self, data):
        phone_number = data["phone_number"]
        password = data["password"]
        user_instance = User.objects.get(phone_number=phone_number)
        user = authenticate(email=user_instance.email, password=password)
        
        if not user:
            raise AuthenticationFailed("رمز عبور یا ایمیل شما صحیح نمی باشد.")

        elif not user.is_active:
            raise AuthenticationFailed("اکانت شما غیر فعال شده است")

        return super().validate(data)