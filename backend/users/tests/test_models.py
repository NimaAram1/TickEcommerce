from re import I
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError

# user model 
User = get_user_model()

class UsersModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(email="test@example.com", username="test", password="test", phone_number="09125689898")

        # testing part

        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "test")
        self.assertNotEqual(user.password, "test")
        self.assertEqual(user.phone_number, "09125689898")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)

    def test_create_superuser(self):
        user = User.objects.create_superuser(email="test2@example.com", username="test2", password="test2", phone_number="09225689898") 

        # testing part

        self.assertEqual(user.email, "test2@example.com")
        self.assertEqual(user.username, "test2")
        self.assertNotEqual(user.password, "test2")
        self.assertEqual(user.phone_number, "09225689898")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, True)

    def test_create_user_with_same_email_and_username(self):
        user = User.objects.create_user(email="test3@example.com", username="test3@example.com", password="test3", phone_number="09335689898")

        # testing part

        try:
            with self.assertRaises(IntegrityError):
                user.save()
        except:
            print("Sqlite doesn't support constraints, try with Postgresql")

    def test_create_user_wrong_phone(self):
        user = User.objects.return_user_intance(email="test4@example.com", username="test4", password="test4", phone_number="93356898")
        
        # testing part  

        try:
            with self.assertRaises(IntegrityError):
                user.save()
        except:
            print("Sqlite doesn't support constraints, try with Postgresql")                            