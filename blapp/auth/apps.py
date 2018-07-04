from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthConfig(AppConfig):
    name = "blapp.auth"
    label = "blapp_auth"
    verbose_name = _("Authentication and authorization")
