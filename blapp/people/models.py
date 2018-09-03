from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from blapp.utils.db_fields import (
    DescriptionField,
    NameField,
    PrimaryKeyUUIDField,
    UniqueEmailField,
)


class Person(models.Model):
    id = PrimaryKeyUUIDField()

    first_name = NameField(verbose_name=_("first name"))
    last_name = NameField(verbose_name=_("last name"))
    nickname = NameField(blank=True, verbose_name=_("nickname"))

    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name=_("date of birth")
    )
    date_of_death = models.DateField(
        null=True, blank=True, verbose_name=_("date of death")
    )

    # Email must be unique if set
    email = UniqueEmailField()

    legacy_id = models.PositiveIntegerField(null=True, blank=True)

    temp_tour18 = models.BooleanField(default=False)

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        return (
            f'{self.first_name} "{self.nickname}" {self.last_name}'
            if self.nickname
            else f"{self.first_name} {self.last_name}"
        )

    @property
    def short_name(self):
        return self.nickname or f"{self.first_name} {self.last_name[:1]}"


class Role(MPTTModel, models.Model):
    id = PrimaryKeyUUIDField()

    name = NameField()
    description = DescriptionField()

    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )

    membership = models.BooleanField(default=False)
    engagement = models.BooleanField(default=False)

    legacy_table = models.CharField(max_length=64)
    legacy_id = models.CharField(max_length=64)

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class RoleAssignment(models.Model):
    id = PrimaryKeyUUIDField()

    role = TreeForeignKey(
        "people.Role",
        on_delete=models.CASCADE,
        related_name="role_assignments",
        verbose_name=_("role"),
    )
    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="role_assignments",
        verbose_name=_("person"),
    )

    period = DateRangeField(verbose_name=_("period"))
    trial = models.BooleanField()

    legacy_table = models.CharField(max_length=64)
    legacy_start_id = models.CharField(max_length=64)
    legacy_end_id = models.CharField(max_length=64)

    class Meta:
        ordering = ["period"]

    def __str__(self):
        return f"{self.person.short_name}: {self.role} ({self.period.lower}–{self.period.upper})"
