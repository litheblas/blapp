import pytest
from django.contrib.auth import authenticate

from blapp.auth.models import UserAccount
from blapp.utils.testing import factories

pytestmark = pytest.mark.django_db


class test_user_account_manager:
    def test_create_user(self):
        user = UserAccount.objects.create_user(
            first_name="first",
            last_name="last",
            email="first@last.com",
            username="firstlast",
            password="abcdefgh",
        )
        user.refresh_from_db()

        assert user.person.first_name == "first"
        assert user.person.last_name == "last"
        assert user.person.email == "first@last.com"
        assert user.username == "firstlast"
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser(self):
        user = UserAccount.objects.create_superuser(
            first_name="first",
            last_name="last",
            email="first@last.com",
            username="firstlast",
            password="abcdefgh",
        )
        user.refresh_from_db()

        assert user.person.first_name == "first"
        assert user.person.last_name == "last"
        assert user.person.email == "first@last.com"
        assert user.username == "firstlast"
        assert user.is_active is True
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_authenticate(self):
        expected_user = UserAccount.objects.create_user(
            first_name="first",
            last_name="last",
            email="first@last.com",
            username="firstlast",
            password="abcdefgh",
        )

        assert (
            authenticate(request=None, username="firstlast", password="wrong") is None
        )
        assert authenticate(request=None, username="dunno", password="abcdefgh") is None
        assert (
            authenticate(request=None, username="firstlast", password="abcdefgh")
            == expected_user
        )


class test_service_account:
    def test_authenticate(self):
        expected_service_account = factories.ServiceAccountFactory(token="goodtoken")

        assert authenticate(request=None, service_token="badtoken") is None
        assert authenticate(request=None, token="goodtoken") is None
        assert (
            authenticate(request=None, service_token="goodtoken")
            == expected_service_account
        )

    def test_authenticate_from_request(self, request_factory):
        expected_service_account = factories.ServiceAccountFactory(token="goodtoken")

        assert (
            authenticate(
                request=request_factory.get(
                    "/",
                    HTTP_AUTHORIZATION="Service-Token badtoken",
                ),
            )
            is None
        )
        assert (
            authenticate(
                request=request_factory.get("/", HTTP_AUTHORIZATION="Token goodtoken"),
            )
            is None
        )
        assert (
            authenticate(
                request=request_factory.get(
                    "/",
                    HTTP_AUTHORIZATION="Service-Token goodtoken",
                ),
            )
            == expected_service_account
        )
