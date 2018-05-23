from graphene import ObjectType, Schema, String
from graphene.relay import Node as RelayNode
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from blapp.auth import models as auth_models
from blapp.people import models as people_models


class Node(RelayNode):
    pass


class Person(DjangoObjectType):
    full_name = String()
    short_name = String()

    class Meta:
        model = people_models.Person
        interfaces = (Node,)
        only_fields = (
            'id',
            'full_name',
            'short_name',
            'first_name',
            'last_name',
            'nickname',
            'date_of_birth',
            'date_of_death',
            'email',
            'legacy_id',
            # Relations
            'user_account',
        )
        filter_fields = []


class UserAccount(DjangoObjectType):
    class Meta:
        model = auth_models.UserAccount
        interfaces = (Node,)
        only_fields = (
            'id',
            'username',
            # Relations
            'person',
        )
        filter_fields = ['username']


class CoreQuery:
    people = DjangoFilterConnectionField(Person)
    person = Node.Field(Person)
    user_accounts = DjangoFilterConnectionField(UserAccount)
    user_account = Node.Field(UserAccount)


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema)
