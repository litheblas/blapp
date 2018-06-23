from django.conf.urls import include, url
from django.contrib import admin
from django.http.response import Http404

from blapp.api.views import api_view


def dummy_view(request):
    raise Http404()


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/graphql/$', api_view, name='api-graphql'),
    url(r'^auth/', include([
        url(r'^', include('django.contrib.auth.urls')),
        url(r'^openid/', include([
            url(r'^', include('oidc_provider.urls', namespace='openid')),
            url(r'$', dummy_view, name='openid'),
        ])),
    ])),
    url(r'^', include('blapp.frontend.urls')),
]
