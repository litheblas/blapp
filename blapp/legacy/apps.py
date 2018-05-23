from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class LegacyConfig(AppConfig):
    name = 'blapp.legacy'
    verbose_name = _('Legacy')
