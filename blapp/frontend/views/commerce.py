from django.conf import settings
from django.shortcuts import render_to_response


def bulk_seller(request):
    return render_to_response(
        template_name='commerce/bulk-seller.html',
        context={
            'APP_SETTINGS': settings.FRONTEND_SETTINGS,
        },
    )
