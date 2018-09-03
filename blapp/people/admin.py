from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from . import models


class RoleAssignmentInline(admin.TabularInline):
    model = models.RoleAssignment
    fields = ["person", "role", "period", "trial"]
    extra = 0


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "nickname", "email"]
    inlines = [RoleAssignmentInline]


@admin.register(models.Role)
class RoleAdmin(MPTTModelAdmin, admin.ModelAdmin):
    list_display = ["name", "description", "membership", "engagement"]
    inlines = [RoleAssignmentInline]
