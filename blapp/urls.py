from django.conf.urls import include, url
from django.contrib import admin

from blapp.api.views import api_view
from blapp.webclient.views import webclient_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/graphql/$', api_view, name='api-graphql'),

    url(r'^$', webclient_view),
]
