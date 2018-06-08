from django.contrib import admin

from . import models


admin.site.register(models.Product)
admin.site.register(models.Purchase)
admin.site.register(models.SalePoint)
