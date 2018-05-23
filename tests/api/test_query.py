import pytest

from blapp.utils.testing.factories import PersonFactory

pytestmark = pytest.mark.django_db


class test_person_query:
    def test_simple(self, schema_client):
        person = PersonFactory.create()
        result = schema_client.execute("""
            {
                people {
                    edges {
                        node {
                            firstName
                            lastName
                            email
                        }
                    }
                }
            }
        """)

        assert result == {
            'data': {
                'people': {
                    'edges': [
                        {
                            'node': {
                                'firstName': person.first_name,
                                'lastName': person.last_name,
                                'email': person.email,
                            },
                        },
                    ],
                },
            },
        }
