from django.contrib import admin
from . import models

@admin.register(models.Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ["header", "date_time"]