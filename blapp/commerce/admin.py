from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price"]


@admin.register(models.Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "person", "product", "quantity"]
    date_hierarchy = "timestamp"


admin.site.register(models.SalePoint)
