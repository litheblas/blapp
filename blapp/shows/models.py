from django.utils.timezone import now
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
    start_date_time = models.DateTimeField(verbose_name=_("start date time"), null=False, default=now)
    end_date_time = models.DateTimeField(verbose_name=_("end date time"), null=False)
    location = NameField(verbose_name=_("location"))
    driving_section = NameField(verbose_name=_("driving section"), blank=True)
    
    contact_person_name = NameField(verbose_name=_("contact person name"), blank=True)
    contact_person_email_address = NameField(verbose_name=_("contact person email address"), blank=True)
    contact_person_phone_number = NameField(verbose_name=_("contact person phone number"), blank=True)
    contact_person_comment = DescriptionField(verbose_name=_("contact person comment"), blank=True)
    comment = DescriptionField(verbose_name=_("comment"), blank=True)
    fee = NameField(verbose_name=_("fee"), blank=True)

    class Meta:
        ordering = ("start_date_time", "header")
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date_time__gt=models.F("start_date_time")),
                name="end_date_time_gte_start_date_time"
            )
        ]

    def __str__(self):
        return self.header