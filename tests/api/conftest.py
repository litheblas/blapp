import pytest
from graphene.test import Client

from blapp.api.schema import schema


@pytest.fixture
def schema_client():
    return Client(schema)
