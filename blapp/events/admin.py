from django.contrib import admin

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["header", "start_date_time"]
