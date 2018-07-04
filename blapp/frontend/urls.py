from django.conf.urls import include, url

from .views.commerce import bulk_seller

# fmt: off
urlpatterns = [
    url(r"^commerce/bulk/", bulk_seller),
]
# fmt: on
