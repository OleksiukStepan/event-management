from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin


admin.site.unregister(User)


@admin.register(User)
class UserAdmin(ModelAdmin, BaseUserAdmin):
    search_fields = ("username", "first_name", "last_name", "email")
    search_help_text = "Search by username, first name, last name, or email"
    list_display = ("id", "username", "email", "first_name", "last_name", "is_staff")
    list_display_links = ("id", "username")
    ordering = ("username",)
    list_filter = ("is_staff", "is_superuser", "is_active")
