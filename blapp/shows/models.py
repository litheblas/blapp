from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _
from blapp.utils.db_fields import (
    DescriptionField,
    PrimaryKeyUUIDField,
    NameField,
)
from blapp.people.models import Person
from blapp.auth.models import UserAccount

class Show(models.Model):
    id = PrimaryKeyUUIDField()

    header = NameField(verbose_name=_("header"))
    description = DescriptionField(verbose_name=_("description"))
    published = models.BooleanField(default=True)
    obligatory = models.BooleanField(default=True, verbose_name=_("obligatory attendance"))
    start_date_time = models.DateTimeField(verbose_name=_("start date time"), null=False, default=now)
    end_date_time = models.DateTimeField(verbose_name=_("end date time"), null=False)
    location = NameField(verbose_name=_("location"))
    responsible_group = NameField(verbose_name=_("responsible group"), blank=True)
    
    creator = models.ForeignKey(UserAccount, related_name=_("event_creator"), verbose_name=_(
        "event creator"), blank=True, null=True, on_delete=models.SET_NULL)
    contact_person_name = NameField(verbose_name=_("contact person name"), blank=True)
    contact_person_email_address = NameField(verbose_name=_("contact person email address"), blank=True)
    contact_person_phone_number = NameField(verbose_name=_("contact person phone number"), blank=True)
    contact_person_comment = DescriptionField(verbose_name=_("contact person comment"), blank=True)
    rating = models.TextField(verbose_name=_("rating"), null=True, blank=True)
    comment = DescriptionField(verbose_name=_("comment"), blank=True)
    price = NameField(verbose_name=_("price"), blank=True)

    attendants = models.ManyToManyField(Person, related_name=("attendants"), through="Attendance")

    class Meta:
        ordering = ("start_date_time", "header")
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date_time__gt=models.F("start_date_time")),
                name="show_end_date_time_gt_start_date_time"
            )
        ]

    def __str__(self):
        return self.header


class Attendance(models.Model):
    id = PrimaryKeyUUIDField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Show, on_delete=models.CASCADE)

    class Meta:
        models.UniqueConstraint(fields=["event", "person"], name="unique-attendant")