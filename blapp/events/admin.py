from django.contrib import admin
from . import models

class EventAttendanceInline(admin.TabularInline):
    model = models.Attendance
    fields = ["person", "event"]
    extra = 0

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["event_name", "creator"]
    inlines = [EventAttendanceInline]

@admin.register(models.Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    readonly_fields = ["person", "event"]
    list_display = ["person", "event"]
    
    def has_add_permission(self, request, obj=None):
        return False