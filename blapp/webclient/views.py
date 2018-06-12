from django.conf import settings
from django.shortcuts import render_to_response


def webclient_view(request):
    return render_to_response(
        template_name='index.html',
        context={
            'WEBCLIENT_SETTINGS': settings.WEBCLIENT_SETTINGS,
        },
    )
