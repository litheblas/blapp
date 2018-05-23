import re

from .models import ServiceAccount


class ServiceAccountTokenBackend:
    def authenticate(self, request, service_token=None):
        if request and not service_token:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if not auth_header:
                return None
            match = re.match(r'^Service-Token (\S*)$', auth_header)
            if not match:
                return None
            service_token = match[1]
        try:
            return ServiceAccount.objects.get(token=service_token)
        except ServiceAccount.DoesNotExist:
            return None
