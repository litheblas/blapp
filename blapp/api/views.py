from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from .schema import schema

_api_view = GraphQLView.as_view(
    schema=schema,
    graphiql=True,
)


@csrf_exempt
def api_view(request):
    return _api_view(request)
