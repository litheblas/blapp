from Cryptodome.PublicKey import RSA
from django.contrib.auth.hashers import make_password
from factory import (
    DjangoModelFactory,
    Faker,
    LazyAttribute,
    LazyFunction,
    SubFactory,
)
from oidc_provider.models import Client, RSAKey

from blapp.auth.models import ServiceAccount, UserAccount
from blapp.people.models import Person
from blapp.utils.random import hex_string


class ClientFactory(DjangoModelFactory):
    name = Faker('company')
    client_id = LazyFunction(lambda: hex_string(64))
    client_secret = LazyFunction(lambda: hex_string(64))

    scopes = ['openid', 'profile', 'email', 'address']
    scope = LazyAttribute(lambda o: ' '.join(o.scopes))

    class Meta:
        model = Client
        exclude = [
            'scopes',
        ]


class RsaKeyFactory(DjangoModelFactory):
    key = LazyFunction(lambda: RSA.generate(1024).exportKey('PEM').decode('utf-8'))

    class Meta:
        model = RSAKey


class PersonFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    date_of_birth = Faker('past_date', start_date='-80y')

    email = Faker('email')

    class Meta:
        model = Person


class UserAccountFactory(DjangoModelFactory):
    person = SubFactory(PersonFactory)
    username = Faker('user_name')
    clear_password = Faker('password')
    password = LazyAttribute(lambda o: make_password(o.clear_password))

    class Meta:
        model = UserAccount
        exclude = [
            'clear_password',
        ]


class ServiceAccountFactory(DjangoModelFactory):
    name = Faker('bs')

    class Meta:
        model = ServiceAccount
