from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# getting user model
User = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
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