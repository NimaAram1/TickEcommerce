from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import RegexValidator
from django.utils.text import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.core.validators import MinLengthValidator as minl, MaxLengthValidator as maxl
from .managers import UserManager
import datetime

class User(AbstractBaseUser):
    """ 
    If you want to have your own database field name,
    you can add "db_column" to them and pick your favorite name    
    """
    email = models.EmailField(max_length=200, unique=True, verbose_name=_("Email"), help_text=_("Enter your email"))
    username = models.CharField(max_length=200, unique=True, verbose_name=_("Username"), help_text=_("Enter your username(English words only)"))
    first_name = models.CharField(max_length=60, verbose_name=_("Name"), help_text=_("Enter your name"), blank=True, null=True)
    last_name = models.CharField(max_length=60, verbose_name=_("Last name"), help_text=_("Enter your last name"), blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True, verbose_name=_("Birth date"), help_text=_("Enter your birth date"))
    phone_number_regex = RegexValidator(regex=r"^09(1[0-9]|2[0-9]|3[0-9])[0-9]{3}[0-9]{4}$")
    phone_number = models.CharField(max_length=11, unique=True, validators=[phone_number_regex, minl(11), maxl(11)], verbose_name=_("Phone number"), help_text=_("Enter your phone number, Be care that your phone number must start with 091"))
    address = models.TextField(blank=True, null=True, verbose_name=_("Address"), help_text=_("Enter your home's address"))
    wallet_stock = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name=_("Wallet stock"))
    favorite_tags = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Favorite tags"))
    user_level = models.IntegerField(blank=True, default=0, verbose_name=_("Your account's level"))
    experiments = models.BigIntegerField(blank=True, default=15, verbose_name=_("Your account's experiences")) 
    premium_until = models.DateTimeField(default=timezone.now, verbose_name=_("Your account is premium until"))
    is_premium = models.BooleanField(default=False, verbose_name=_("Is your account premium"))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
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
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        indexes = [
            models.Index(name="email_index", fields=["email"])
        ]
        constraints = [
            models.CheckConstraint(name="check_birth_date", check=Q(birth_date__lt=f"{datetime.date.today()}")),
            models.CheckConstraint(name="check_phone_number", check=Q(phone_number__regex=r"^09(1[0-9]|2[0-9]|3[0-9])[0-9]{3}[0-9]{4}$")),
            models.UniqueConstraint(name="username_email_unique", fields=["username", "email"])
        ]    