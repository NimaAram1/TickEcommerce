from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils import timezone
from django.db.models import Q
import datetime

class User(AbstractBaseUser):
    """ 
    If you want to have your own database field name,
    you can add "db_column" to them and pick your favorite name    
    """
    email = models.EmailField(max_length=200, unique=True, verbose_name="ایمیل", help_text="ایمیل خود را وارد کنید")
    username = models.CharField(max_length=200, unique=True, verbose_name="نام کاربری", help_text="نام کاربری خود را با حروف انگلیسی وارد کنید")
    first_name = models.CharField(max_length=60, verbose_name="نام", help_text="نام خود را وارد کنید", blank=True, null=True)
    last_name = models.CharField(max_length=60, verbose_name="نام خانوادگی", help_text="نام خانوادگی خود را وارد کنید", blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تولد", help_text="تاریخ تولد خود را وارد نمایید")
    phone_number_regex = RegexValidator(regex=r"^09(1[0-9]|2[0-9]|3[0-9])[0-9]{3}[0-9]{4}$")
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_number_regex], verbose_name="شماره موبایل", help_text="شماره موبایل خود را بهمراه صفر اول آن را وارد کنید")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس منزل", help_text="آدرس منزل را در صورت تمایل وارد نمایید")
    wallet_stock = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="موجودی کیف پول")
    favorite_tags = models.CharField(max_length=100, null=True, blank=True, verbose_name="تگ های مورد علاقه")
    user_level = models.IntegerField(blank=True, default=0, verbose_name="سطح حساب شما")
    experiments = models.BigIntegerField(blank=True, default=15, verbose_name="میزان تجربه کاربری") 
    premium_until = models.DateTimeField(default=timezone.now, verbose_name="تا چه زمانی کاربر ویژه هستید")
    is_premium = models.BooleanField(default=False, verbose_name="آیا کاربر ویژه هستید؟")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "phone_number"]

    def __str__(self):
        return f"{self.username} | {self.email}"

    def is_premium_user(self):
        if self.premium_until > timezone.now():
            self.is_premium = True
            return True
        else:
            self.is_premium = False
            return False

    def has_perm(self, perm, obj=None):
        return True


    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin    

    class Meta:
        verbose_name = "حساب"
        verbose_name_plural = "حساب های کاربری"
        indexes = [
            models.Index(name="email_index", fields=["email"])
        ]
        constraints = [
            models.CheckConstraint(name="check_birth_date", check=Q(birth_date__lt=f"{datetime.date.today()}")),
            models.UniqueConstraint(name="username_email_unique", fields=["username", "email"])
        ]    