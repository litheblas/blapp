from factory import DjangoModelFactory, Faker, SubFactory

from blapp.auth.models import ServiceAccount, UserAccount
from blapp.people.models import Person


class PersonFactory(DjangoModelFactory):
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    date_of_birth = Faker('past_date', start_date='-80y')

    email = Faker('email')

    class Meta:
        model = Person


class UserAccountFactory(DjangoModelFactory):
    person = SubFactory(PersonFactory)

    class Meta:
        model = UserAccount


class ServiceAccountFactory(DjangoModelFactory):
    name = Faker('bs')

    class Meta:
        model = ServiceAccount
