from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import (
    RegisterationSerializer,
    LoginSerializerViaEmail,
    LoginSerializerViaPhoneNumber
)

# getting user model
User = get_user_model()

class TestRegistrationSerializer(TestCase):
    def test_serialize_user(self):
        user = User.objects.create_user(email="test@example.com", username="test", password="testbadtest", phone_number="09128007000")
        serialized_user = RegisterationSerializer(user)

        # testing part

        self.assertEqual(
            User.objects.get(username=serialized_user.data["username"]), user, "Serializer didn't work")
        self.assertEqual(
            serialized_user.data["email"], "test@example.com", "Serializer didn't work")
        self.assertEqual(
            serialized_user.data["phone_number"], "09128007000", "Serializer didn't work")

class TestLoginSerializer(TestCase):
    def test_login_via_email(self):
        User.objects.create_user(email="test@example.com", username="test", phone_number="09226000300", password="superpowerfulpassword")
        serialized_user = LoginSerializerViaEmail(data={"email":"test@example.com", "password":"superpowerfulpassword"})
        
        # testing part
        
        self.assertTrue(serialized_user.is_valid())


    def test_login_via_phone_number(self):
        User.objects.create_user(email="test2@example.com", username="test2", phone_number="09226000400", password="superpowerfulpassword")
        serialized_user = LoginSerializerViaPhoneNumber(data={"phone_number":"09226000400", "password":"superpowerfulpassword"})
        
        # testing part

        self.assertTrue(serialized_user.is_valid())