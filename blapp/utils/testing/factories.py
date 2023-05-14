from Cryptodome.PublicKey import RSA
from django.contrib.auth.hashers import make_password
from factory import Faker, LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from oidc_provider.models import Client, RSAKey

from blapp.auth.models import ServiceAccount, UserAccount
from blapp.people.models import Person
from blapp.utils.random import hex_string


class ClientFactory(DjangoModelFactory):
    name = Faker("company")
    client_id = LazyFunction(lambda: hex_string(64))
    client_secret = LazyFunction(lambda: hex_string(64))

    scopes = ["openid", "profile", "email", "address"]
    scope = LazyAttribute(lambda o: " ".join(o.scopes))

    class Meta:
        model = Client
        exclude = ["scopes"]


class RsaKeyFactory(DjangoModelFactory):
    key = LazyFunction(lambda: RSA.generate(1024).exportKey("PEM").decode("utf-8"))

    class Meta:
        model = RSAKey


class PersonFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    nickname = Faker("first_name")

    date_of_birth = Faker("past_date", start_date="-80y")
    date_of_death = Faker("past_date", start_date="-60y")

    email = Faker("email")

    street_address = Faker("street_address")
    postal_code = Faker("postcode")
    postal_region = Faker("city")
    country = Faker("country")
    national_id_number = fuzzy.FuzzyText(length=4, chars="0123456789")
    student_id = LazyAttribute(
        lambda o: "{}".format(o.first_name)[:3].lower()
        + "{}".format(o.last_name)[:2].lower()
        + "{}".format(o.national_id_number)[:3],
    )
    dietary_preferences = Faker("color_name")
    arbitrary_text = Faker("paragraph")
    phone_number_1 = Faker("phone_number")
    phone_number_1_label = Faker("word")
    phone_number_2 = Faker("phone_number")
    phone_number_2_label = Faker("word")
    phone_number_3 = Faker("phone_number")
    phone_number_3_label = Faker("word")

    class Meta:
        model = Person


class UserAccountFactory(DjangoModelFactory):
    person = SubFactory(PersonFactory)
    username = Faker("user_name")
    clear_password = Faker("password")
    password = LazyAttribute(lambda o: make_password(o.clear_password))

    class Meta:
        model = UserAccount
        exclude = ["clear_password"]


class ServiceAccountFactory(DjangoModelFactory):
    name = Faker("bs")

    class Meta:
        model = ServiceAccount
