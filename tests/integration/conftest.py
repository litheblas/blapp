import os

import psutil
import pytest
from django.urls import reverse as django_reverse

from blapp.utils.testing.processes import (
    ExternalProcess,
    ExternalProcessWebserver,
    http_is_responding,
)


@pytest.fixture
def settings_env_prefix():
    return 'BLAPP_'


@pytest.fixture
def service_env(django_db_setup, settings, settings_env_prefix):
    # This will be the *test* database.
    test_db = settings.DATABASES['default'].copy()
    test_db.setdefault('PORT', 0)

    env = os.environ.copy()
    env[f'{settings_env_prefix}DATABASE_URL'] = 'postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'.format(**test_db)

    return env


@pytest.fixture
def webserver(port_getter, service_env):
    port = port_getter()
    url = f'http://127.0.0.1:{port}'

    def start_process():
        return psutil.Popen(
            [
                'daphne',
                '-b0.0.0.0',
                f'-p{port}',
                'blapp.routing:application',
            ],
            # stdin=subprocess.PIPE,
            stdout=None,
            stderr=None,
            env=service_env,
        )

    with ExternalProcess(
        name='webserver',
        start_process=start_process,
        is_ready=http_is_responding(f'{url}/admin/'),
    ) as ext_proc:
        yield ExternalProcessWebserver(
            url=url,
            external_process=ext_proc,
        )


@pytest.fixture
def reverse(webserver):
    return lambda *args, **kwargs: f'{webserver.url}{django_reverse(*args, **kwargs)}'
