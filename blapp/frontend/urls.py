from django.urls import include, re_path

from .views.commerce import bulk_seller

# fmt: off
urlpatterns = [
    re_path(r"^commerce/bulk/", bulk_seller),
]
# fmt: on
