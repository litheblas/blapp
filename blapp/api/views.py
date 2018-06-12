from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from blapp.auth.models import ServiceAccount
from blapp.auth.utils import token_from_request

from .schema import schema

_api_view = GraphQLView.as_view(
    schema=schema,
    graphiql=True,
)


@csrf_exempt
def api_view(request):
    try:
        service_account = ServiceAccount.objects.get(token=token_from_request(request))
        request.user = service_account
    except ServiceAccount.DoesNotExist as exc:
        return HttpResponseBadRequest('Meh. Please log in.', status=401)

    return _api_view(request)
