from django.contrib import admin
from . import models

class ShowAttendanceInline(admin.TabularInline):
    model = models.Attendance
    fields = ["person", "event"]
    extra = 0

@admin.register(models.Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ["header", "start_date_time", "end_date_time"]
    inlines = [ShowAttendanceInline]