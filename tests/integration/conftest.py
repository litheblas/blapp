import pytest
from django.urls import reverse as django_reverse

from blapp.utils.testing.browser import ExternalWebserver


@pytest.fixture
def splinter_webdriver():
    return 'remote'


@pytest.fixture(scope='session')
def splinter_remote_url(env):
    return env.str('TEST_SELENIUM_URL')


@pytest.fixture
def webserver(django_db_setup, env):
    return ExternalWebserver(
        url=env.str('TEST_WEBSERVER_URL'),
    )


@pytest.fixture
def reverse(webserver):
    return lambda *args, **kwargs: f'{webserver.url}{django_reverse(*args, **kwargs)}'
