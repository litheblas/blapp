import uuid

from graphene import ID, DateTime, Date, Field, Int, ObjectType, Schema, String
from graphene.relay import Node as RelayNode
from graphene.relay import ClientIDMutation
from graphene.types import interface
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from blapp.auth import models as auth_models
from blapp.commerce import models as commerce_models
from blapp.people import models as people_models
from blapp.events import models as event_models


class Node(RelayNode):
    pass


class UserAccount(DjangoObjectType):
    class Meta:
        model = auth_models.UserAccount
        interfaces = [Node]
        only_fields = [
            "id",
            "username",
            # Relations
            "person",
        ]
        filter_fields = ["username"]


class Product(DjangoObjectType):
    class Meta:
        model = commerce_models.Product
        interfaces = [Node]
        only_fields = ["id", "name", "description", "price"]
        filter_fields = []


class SalePoint(DjangoObjectType):
    class Meta:
        model = commerce_models.SalePoint
        interfaces = [Node]
        only_fields = ["id", "name", "description"]
        filter_fields = []


class Purchase(DjangoObjectType):
    class Meta:
        model = commerce_models.Purchase
        interfaces = [Node]
        only_fields = [
            "id",
            "uid",
            "quantity",
            "timestamp",
            # Relations
            "person",
            "product",
            "sale_point",
        ]
        filter_fields = []


class Person(DjangoObjectType):
    full_name = String()
    short_name = String()

    class Meta:
        model = people_models.Person
        interfaces = [Node]
        only_fields = [
            "id",
            "full_name",
            "short_name",
            "first_name",
            "last_name",
            "nickname",
            "date_of_birth",
            "date_of_death",
            "email",
            "legacy_id",
            # Relations
            "purchases",
            "user_account",
        ]
        filter_fields = ["temp_tour18"]


class EditPerson(ClientIDMutation):
    person = Field(lambda: Person)
    
    class Input:
        uid = String()
        first_name = String()
        last_name = String()
        nickname = String()
        # date_of_birth = Date()
        # date_of_death = Date()
        # email = String()
        # legacy_id = Int()
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        person = people_models.Person.objects.get(id=uuid.UUID(input["uid"]))
        person.first_name = input["first_name"]
        person.last_name = input["last_name"]
        person.nickname = input["nickname"]
        #person.date_of_birth = input["date"]
        person.save()

        return EditPerson(person=person)

class MakePurchase(ClientIDMutation):
    purchase = Field(lambda: Purchase)

    class Input:
        uid = String()
        product = ID()
        person = ID()
        sale_point = ID()
        quantity = Int()
        timestamp = DateTime()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        purchase = commerce_models.Purchase(uid=uuid.UUID(input["uid"]))
        purchase.product = Node.get_node_from_global_id(info, input["product"])
        purchase.person = Node.get_node_from_global_id(info, input["person"])
        purchase.sale_point = Node.get_node_from_global_id(info, input["sale_point"])
        purchase.timestamp = input["timestamp"]
        purchase.quantity = input["quantity"]
        purchase.save()

        return MakePurchase(purchase=purchase)


class Event(DjangoObjectType):
    class Meta:
        model = event_models.Event
        interfaces = [Node]
        only_fields = [
            "id",
            "event_name",
            "event_description",
            "published",
            "obligatory",
            "starts",
            "ends",
            "signup_deadline",
            # Relations
            "event_creator",
            "attendances"
        ]
        filter_fields = []

class CreateEvent(ClientIDMutation):
    class Input:
        event_name = String()
        event_description = String()
    
    event = Field(lambda: Event)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = event_models.Event(event_name=input["event_name"], event_description=input["event_description"])
        event.save()
        return CreateEvent(event=event)

class CoreQuery:
    people = DjangoFilterConnectionField(Person)
    person = Node.Field(Person)
    products = DjangoFilterConnectionField(Product)
    product = Node.Field(Product)
    purchases = DjangoFilterConnectionField(Purchase)
    purchase = Node.Field(Purchase)
    sale_points = DjangoFilterConnectionField(SalePoint)
    sale_point = Node.Field(SalePoint)
    user_accounts = DjangoFilterConnectionField(UserAccount)
    user_account = Node.Field(UserAccount)
    events = DjangoFilterConnectionField(Event)
    event = Node.Field(Event)


class CoreMutation(ObjectType):
    make_purchase = MakePurchase.Field()
    create_event = CreateEvent.Field()
    edit_person = EditPerson.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
