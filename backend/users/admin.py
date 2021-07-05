from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .forms import UserCreateFormAdmin, UserChangeFormAdmin

# getting user model
User = get_user_model()

class UserAdmin(BaseAdmin):
    add_form = UserCreateFormAdmin
    form = UserChangeFormAdmin
    list_display = ["email", "username", "user_level", "is_premium", "phone_number"]
    list_filter = ["is_admin", "is_premium"]
    fieldsets = (
        (None, {"fields":["email", "username", "first_name", "last_name"]}),
        ("اطلاعات بیشتر", {"fields":["birth_date", "phone_number", "address", "wallet_stock"]}),
        ("اطلاعات شخصی و دسترسی ها", {"fields":["password", "is_admin", "is_active"]})
    )
    add_fieldsets = (
        (None, {"fields":["email", "username", "phone_number", "password", "repeated_password"]})
    )
    search_fields = ["email", "username", "phone_number"]
    ordering = ["is_premium", "user_level"]
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)