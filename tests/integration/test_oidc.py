from types import SimpleNamespace

import pytest
from oic.oic import Client
from oic.oic.message import AuthorizationResponse, RegistrationResponse
from oic.utils.authn.client import CLIENT_AUTHN_METHOD

from blapp.utils.random import hex_string
from blapp.utils.testing.factories import (
    ClientFactory,
    PersonFactory,
    RsaKeyFactory,
    UserAccountFactory,
)

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def user_password():
    return hex_string(16)


@pytest.fixture
def person():
    return PersonFactory.create()


@pytest.fixture
def user_account(person, user_password):
    return UserAccountFactory.create(person=person, clear_password=user_password)


@pytest.fixture
def oidc_rsa_key():
    return RsaKeyFactory.create()


@pytest.fixture
def oidc_scopes():
    return ["openid", "profile", "email", "address"]


@pytest.fixture
def oidc_provider(oidc_rsa_key, oidc_scopes, webserver):
    client = ClientFactory.create(
        client_type="confidential",
        response_type="code",
        scopes=oidc_scopes,
        jwt_alg="HS256",
    )
    # This URL doesn't have to exist, we will get the redirect URL from the
    # browser anyway
    client.redirect_uris = [f"{webserver.url}/__non-existing_url__/"]
    client.save()

    return client


@pytest.fixture
def oidc_client(webserver, oidc_provider, reverse):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    client.provider_config(issuer=reverse("openid"))
    client.store_registration_info(
        RegistrationResponse(
            client_id=oidc_provider.client_id,
            client_secret=oidc_provider.client_secret,
        ),
    )

    return client


def test_oidc(
    browser,
    oidc_client,
    oidc_provider,
    oidc_scopes,
    person,
    user_account,
    user_password,
):
    oidc_session = SimpleNamespace(state=hex_string(16), nonce=hex_string(16))

    auth_req = oidc_client.construct_AuthorizationRequest(
        request_args={
            "client_id": oidc_client.client_id,
            "response_type": "code",
            "scope": oidc_scopes,
            "nonce": oidc_session.nonce,
            "redirect_uri": oidc_provider.redirect_uris[0],
            "state": oidc_session.state,
        },
    )
    auth_url = auth_req.request(oidc_client.authorization_endpoint)

    browser.visit(auth_url)
    browser.find_by_name("username").fill(user_account.username)
    browser.find_by_name("password").fill(user_password)
    browser.find_by_value("Log in").click()
    browser.find_by_value("Authorize").click()

    auth_resp = oidc_client.parse_response(
        AuthorizationResponse,
        info=browser.url,
        sformat="urlencoded",
    )

    assert auth_resp["state"] == oidc_session.state

    oidc_client.do_access_token_request(
        state=oidc_session.state,
        request_args={"code": auth_resp["code"]},
        authn_method="client_secret_basic",
    )

    user_info = oidc_client.do_user_info_request(
        state=oidc_session.state,
        behavior="use_authorization_header",
    )

    assert user_info["sub"] == str(user_account.pk)
    assert user_info["name"] == person.full_name
    assert user_info["given_name"] == person.first_name
    assert user_info["family_name"] == person.last_name
    if person.nickname:
        assert user_info["nickname"] == person.nickname
    assert user_info["preferred_username"] == user_account.username
    assert user_info["birthdate"] == person.date_of_birth.isoformat()
    assert user_info["email"] == person.email
