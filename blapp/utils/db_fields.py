import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class PrimaryKeyUUIDField(models.UUIDField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', uuid.uuid4)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('primary_key', True)
        kwargs.setdefault('verbose_name', _('ID'))
        super().__init__(*args, **kwargs)


class DescriptionField(models.TextField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('verbose_name', _('description'))
        super().__init__(*args, **kwargs)


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 256)
        kwargs.setdefault('verbose_name', _('name'))
        super().__init__(*args, **kwargs)


class UniqueEmailField(models.EmailField):
    def __init__(self, *args, **kwargs):
        kwargs['blank'] = True
        kwargs['default'] = None
        kwargs['null'] = True
        kwargs['unique'] = True
        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        # Makes sure that blank values gets saved as None/NULL and in a
        # normalized form. The lowercase method of normalizing is a bit crude
        # but probably works good enough.
        value = super().clean(*args, **kwargs)
        return value.lower() if value else None


class MoneyDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 12
        kwargs['decimal_places'] = 2
        super().__init__(*args, **kwargs)
