from django.conf.urls import url
from django.contrib import admin

from blapp.api.views import api_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/graphql/$', api_view, name='api-graphql'),
]
