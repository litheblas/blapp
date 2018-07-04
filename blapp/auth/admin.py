from django.contrib import admin

from . import models


class ServiceAccountAdmin(admin.ModelAdmin):
    readonly_fields = ["token"]


admin.site.register(models.ServiceAccount, ServiceAccountAdmin)
