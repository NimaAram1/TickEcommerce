from django.test import TestCase
from django.contrib.auth import get_user_model
from ..serializers import RegisterationSerializer

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
        self.assertNotEqual(
            serialized_user.data["password"], "testbadtest", "Serializer didn't work")
        self.assertEqual(
            serialized_user.data["phone_number"], "09128007000", "Serializer didn't work")        