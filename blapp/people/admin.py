from django.contrib import admin

from . import models


class PersonAdmin(admin.ModelAdmin):
    search_fields = ["first_name", "last_name", "nickname", "email"]


admin.site.register(models.Person, PersonAdmin)
