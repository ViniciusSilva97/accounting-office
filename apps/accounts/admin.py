from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class OfficeUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ["email", "full_name", "office", "role", "is_active"]
    list_filter = ["office", "role", "is_active"]
    search_fields = ["email", "full_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Escritório", {"fields": ("office", "full_name", "role")}),
        ("Acesso", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Permissões", {"fields": ("groups", "user_permissions")}),
        ("Datas", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "office", "role", "password1", "password2"),
            },
        ),
    )
