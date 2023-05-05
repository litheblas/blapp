from django.conf import settings
from django.shortcuts import render


def bulk_seller(request):
    return render(
        request=request,
        template_name="commerce/bulk-seller.html",
        context={"APP_SETTINGS": settings.FRONTEND_SETTINGS},
    )
