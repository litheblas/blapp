import pytest
from django.test import RequestFactory

from blapp.utils.testing.factories import UserAccountFactory

pytestmark = pytest.mark.django_db
date_format = "%Y-%m-%d"


class test_person_query:
    def test_simple(self, schema_client):
        user = UserAccountFactory.create()
        request_factory = RequestFactory()
        context_value = request_factory.request()
        context_value.user = user
        result = schema_client.execute(
            """
            {
                people {
                    edges {
                        node {
                            firstName
                            lastName
                            nickname
                            dateOfBirth
                            dateOfDeath
                            email
                            streetAddress
                            postalCode
                            postalRegion
                            country
                            nationalIdNumber
                            studentId
                            dietaryPreferences
                            arbitraryText
                            phoneNumber1
                            phoneNumber1Label
                            phoneNumber2
                            phoneNumber2Label
                            phoneNumber3
                            phoneNumber3Label
                        }
                    }
                }
            }
        """,
            context_value=context_value,
        )

        assert result == {
            "data": {
                "people": {
                    "edges": [
                        {
                            "node": {
                                "firstName": user.person.first_name,
                                "lastName": user.person.last_name,
                                "nickname": user.person.nickname,
                                "dateOfBirth": user.person.date_of_birth.strftime(
                                    date_format,
                                ),
                                "dateOfDeath": user.person.date_of_death.strftime(
                                    date_format,
                                ),
                                "email": user.person.email,
                                "streetAddress": user.person.street_address,
                                "postalCode": user.person.postal_code,
                                "postalRegion": user.person.postal_region,
                                "country": user.person.country,
                                "nationalIdNumber": user.person.national_id_number,
                                "studentId": user.person.student_id,
                                "dietaryPreferences": user.person.dietary_preferences,
                                "arbitraryText": user.person.arbitrary_text,
                                "phoneNumber1": user.person.phone_number_1,
                                "phoneNumber1Label": user.person.phone_number_1_label,
                                "phoneNumber2": user.person.phone_number_2,
                                "phoneNumber2Label": user.person.phone_number_2_label,
                                "phoneNumber3": user.person.phone_number_3,
                                "phoneNumber3Label": user.person.phone_number_3_label,
                            },
                        },
                    ],
                },
            },
        }
