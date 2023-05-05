from django.contrib import admin
from django.http.response import Http404
from django.urls import include, re_path

from blapp.api.views import api_view


def dummy_view(request):
    raise Http404()


# fmt: off
urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^api/graphql/$", api_view, name="api-graphql"),
    re_path(r"^o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    re_path(
        r"^auth/", include([
            re_path(r"^", include("django.contrib.auth.urls")),
            re_path(
                r"^openid/", include([
                    re_path(r"^", include("oidc_provider.urls", namespace="openid")),
                    re_path(r"$", dummy_view, name="openid"),
                ]),
            ),
        ]),
    ),
    re_path(r"", include("blapp.frontend.urls")),
]
# fmt: on
