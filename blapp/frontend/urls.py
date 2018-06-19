from django.conf.urls import include, url

from .views.commerce import bulk_seller

urlpatterns = [
    url(r'^commerce/bulk/', bulk_seller),
]
