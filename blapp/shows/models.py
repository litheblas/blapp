from datetime import datetime, timedelta
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models
from django.utils.translation import gettext_lazy as _
from blapp.utils.db_fields import (
    DescriptionField,
    PrimaryKeyUUIDField,
    NameField,
)

class Show(models.Model):
    id = PrimaryKeyUUIDField()

    header = NameField(verbose_name=_("header"))
    description = DescriptionField(verbose_name=_("description"))
    date_time = DateTimeRangeField(verbose_name=_("date and time"), default=(datetime.now().replace(second=0), datetime.now().replace(second=0) + timedelta(hours=1)))
    location = NameField(verbose_name=_("location"))
    driving_section = NameField(blank=True, verbose_name=_("driving section"))
    contact_person_name = NameField(blank=True, verbose_name=_("contact person name"))
    contact_person_email_address = NameField(blank=True, verbose_name=_("contact person email address"))
    contact_person_phone_number = NameField(blank=True, verbose_name=_("contact person phone number"))
    fee = NameField(blank=True, verbose_name=_("fee"))

    class Meta:
        ordering = ("date_time", "header")

    def __str__(self):
        return self.header