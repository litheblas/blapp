from django.utils.timezone import now
from django.db import models
from django.utils.translation import gettext_lazy as _
from blapp.utils.db_fields import (
    DescriptionField,
    PrimaryKeyUUIDField,
    NameField
)

class Event(models.Model):
    id = PrimaryKeyUUIDField()

    header = NameField(verbose_name=_("header"))
    description = DescriptionField(verbose_name=_("description"))
    location = NameField(verbose_name=_("location"))
    start_date_time = models.DateTimeField(verbose_name=_("start date time"), null=False, default=now)
    end_date_time = models.DateTimeField(verbose_name=_("end date time"), null=False)

    class Meta:
        ordering = ("start_date_time", "header")
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date_time__gt=models.F("start_date_time")),
                name="event_end_date_time_gt_start_date_time"
            )
        ]
    
    def __str__(self):
        return self.header
