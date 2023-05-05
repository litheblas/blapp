from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.ServiceAccount)
class ServiceAccountAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    readonly_fields = ["token"]


@admin.register(models.UserAccount)
class UserAccountAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("person",)}),
        (
            _("Permissions"),
            {
                "classes": ["collapse"],
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    list_display = ("username", "email", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = (
        "username",
        "person__first_name",
        "person__last_name",
        "person__email",
    )
