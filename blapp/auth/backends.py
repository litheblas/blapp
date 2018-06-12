from .models import ServiceAccount
from .utils import token_from_request


class ServiceAccountTokenBackend:
    def authenticate(self, request, service_token=None):
        if request and not service_token:
            service_token = token_from_request(request)
        try:
            return ServiceAccount.objects.get(token=service_token)
        except ServiceAccount.DoesNotExist:
            return None
