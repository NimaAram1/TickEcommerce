from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    create_user for creating normal permission user
    create_superuser for creating admin user
    return_user_instance for returning user instance for testing in test_models 
    """

    def create_user(self, email, username, password, phone_number):
        if not email:
            raise ValueError("در ساخت حساب ایمیل خود را وارد نمایید")
        elif not username:
            raise ValueError("در ساخت حساب نام کاربری خود را وارد نمایید")
        elif not phone_number:
            raise ValueError("شماره تلفن خود را میبایستی وارد نمایید")
            
        user = self.model(email=self.normalize_email(email), username=username, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db) 
        return user 

    def create_superuser(self, email, username, password, phone_number):
        user = self.create_user(email, username, password, phone_number)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def return_user_intance(self, email, username, password, phone_number):
        user = self.model(email=self.normalize_email(email), username=username, phone_number=phone_number)
        user.set_password(password)
        return user              