from datetime import datetime
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils.translation import ugettext_lazy as _
from blapp.utils.db_fields import (
    DescriptionField,
    PrimaryKeyUUIDField,
    NameField,
)
from blapp.people.models import Person

class Event(models.Model):
    id = PrimaryKeyUUIDField()
    event_name = NameField(verbose_name=_("event name"))
    event_description = DescriptionField()
    published = models.BooleanField(default=True)
    obligatory = models.BooleanField(default=True, verbose_name=_("obligatory attendance"))
    starts = models.DateTimeField(verbose_name=_("start date"), default=datetime.now())
    ends = models.DateTimeField(verbose_name=_("end date"), null=True, blank=True)
    signup_deadline = models.DateTimeField(verbose_name=_("signup deadline"), null=True, blank=True)
    creator = models.ForeignKey(Person, related_name=_("event_creator"), verbose_name=_("event creator"), blank=True, null=True, on_delete=models.SET_NULL)

    attendants = models.ManyToManyField(Person, related_name=("attendants"), through="Attendance")

    def __str__(self):
        return self.event_name

    # tillgångskontroll: bara evenemangskaparen kan hämta ett evenemang som ej är publicerat.


class Attendance(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)