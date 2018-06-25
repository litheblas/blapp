import pytest
from django.conf import settings
from django.test import RequestFactory
from django_redis import get_redis_connection

from blapp.utils.settings import PrefixEnv


@pytest.fixture(scope='session')
def env():
    return PrefixEnv(prefix=settings.ENV_PREFIX)


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture(autouse=True)
def clear_cache():
    get_redis_connection('default').flushall()
