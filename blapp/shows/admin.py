from django.contrib import admin
from . import models

@admin.register(models.Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ["header", "start_date_time", "end_date_time"]