from django.contrib.postgres.fields import DateRangeField
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from blapp.utils.db_fields import (
    DescriptionField,
    NameField,
    PrimaryKeyUUIDField,
    UniqueEmailField,
)

class PhoneNumber(models.Model):
    id = PrimaryKeyUUIDField()

    person = models.ForeignKey(to="Person", on_delete=models.CASCADE, related_name="phone_numbers", verbose_name=_("person"))

    label = models.CharField(verbose_name=_("label"), max_length=20)
    phone_number = models.CharField(verbose_name=_("phone number"), max_length=14)

    def save(self, *args, **kwargs):
        if self.__class__.objects.filter(person=self.person).count() >= 3:
            return
        super().save(*args, **kwargs)

    def __str__(self):
        return "{}: {}, {}".format(self.person.full_name, self.label, self.phone_number)

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
    street_address = NameField(verbose_name=_("street address"), blank=True)
    postal_code = models.CharField(verbose_name=_("postal code"), blank=True, max_length=7)
    postal_region = NameField(verbose_name=_("postal region"), blank=True)
    country = NameField(verbose_name=_("country"), blank=True)
    national_id_number = models.CharField(verbose_name=_("national id number"), blank=True, max_length=4)
    student_id = models.CharField(verbose_name=_("student id"), blank=True, max_length=10)
    dietary_preferences = NameField(verbose_name=_("dietary preferences"), blank=True)
    arbitrary_text = DescriptionField(verbose_name=_("arbitrary text"), blank=True)

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

    legacy_table = models.CharField(max_length=64, blank=True)
    legacy_id = models.CharField(max_length=64, blank=True)

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

    legacy_table = models.CharField(max_length=64, blank=True)
    legacy_start_id = models.CharField(max_length=64, blank=True)
    legacy_end_id = models.CharField(max_length=64, blank=True)

    class Meta:
        ordering = ["period"]

    def __str__(self):
        return f"{self.person.short_name}: {self.role} ({self.period.lower}–{self.period.upper})"
