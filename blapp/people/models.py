from django.db import models
from django.utils.translation import ugettext_lazy as _

from blapp.utils.db_fields import (
    NameField,
    PrimaryKeyUUIDField,
    UniqueEmailField,
)


class Person(models.Model):
    id = PrimaryKeyUUIDField()

    first_name = NameField(verbose_name=_('first name'))
    last_name = NameField(verbose_name=_('last name'))
    nickname = NameField(blank=True, verbose_name=_('nickname'))

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('date of birth'),
    )
    date_of_death = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('date of death'),
    )

    # Email must be unique if set
    email = UniqueEmailField()

    legacy_id = models.PositiveIntegerField(null=True, blank=True)

    temp_tour18 = models.BooleanField(default=False)

    class Meta:
        ordering = ('first_name', 'last_name')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return (
            f'{self.first_name} "{self.nickname}" {self.last_name}'
            if self.nickname else
            f'{self.first_name} {self.last_name}'
        )

    @property
    def short_name(self):
        return self.nickname or f'{self.first_name} {self.last_name[:1]}'
