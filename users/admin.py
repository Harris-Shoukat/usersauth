from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,Profile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff")


admin.site.register(Profile)
