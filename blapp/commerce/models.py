import uuid

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from blapp.utils.db_fields import (
    DescriptionField,
    MoneyDecimalField,
    NameField,
    PrimaryKeyUUIDField,
)


class SalePoint(models.Model):
    id = PrimaryKeyUUIDField()

    name = NameField()
    description = DescriptionField()

    def __str__(self):
        return self.name


class Product(models.Model):
    id = PrimaryKeyUUIDField()

    name = NameField()
    description = DescriptionField()

    price = MoneyDecimalField(null=True, blank=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    id = PrimaryKeyUUIDField()
    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid1,
        help_text=_(
            "Unique ID used to ensure that offline clients can sync multiple "
            "times without creating duplicates. Offline clients *must* supply "
            "this."
        ),
    )

    timestamp = models.DateTimeField(
        default=now, editable=False, verbose_name=_("timestamp")
    )

    person = models.ForeignKey(
        "people.Person",
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name=_("person"),
    )
    product = models.ForeignKey(
        "commerce.Product",
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name=_("product"),
    )
    quantity = models.IntegerField(default=1, verbose_name=_("quantity"))
    sale_point = models.ForeignKey(
        "commerce.SalePoint",
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name=_("sale point"),
    )

    class Meta:
        ordering = ("-timestamp",)
        verbose_name = _("purchase")
        verbose_name_plural = _("purchases")
