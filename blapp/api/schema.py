import uuid

from graphene import ID, DateTime, Date, Field, Int, ObjectType, Schema, String, Boolean
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
        uid = String(required=True)
        first_name = String(default=None)
        last_name = String(default=None)
        nickname = String(default=None)
        date_of_birth = Date(default=None)
        date_of_death = Date(default=None)
        email = String(default=None)
        legacy_id = Int(default=None)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        person = people_models.Person.objects.get(id=uuid.UUID(input["uid"]))
        if input.get("first_name"):
            person.first_name = input["first_name"]
        if input.get("last_name"):
            person.last_name = input["last_name"]
        if input.get("nickname"):
            person.nickname = input["nickname"]
        if input.get("date_of_birth"):
            person.date_of_birth = input["date_of_birth"]
        if input.get("date_of_death"):
            person.date_of_death = input["date_of_death"]
        if input.get("email"):
            person.email = input["email"]
        if input.get("legacy_id"):
            person.legacy_id = input["legacy_id"]
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
            "creator",
            "attendants"
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

class EditEvent(ClientIDMutation):
    event = Field(lambda: Event)
    creator = Field(lambda: Person)
    
    class Input:
        eventUid = String(required=True)
        creatorUid = String(default=None)
        event_name = String(default=None)
        event_description = String(default=None)
        published = Boolean(default=None)
        obligatory = Boolean(default=None)
        starts = DateTime(default=None)
        ends = DateTime(default=None)
        signup_deadline = DateTime(default=None)
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = event_models.Event.objects.get(id=uuid.UUID(input["eventUid"]))
        if input.get("creatorUid"):
            creator = people_models.Person.objects.get(id=uuid.UUID(input["creatorUid"]))
            event.creator = creator

        if input.get("event_name"):
            event.event_name = input.get("event_name")
        if input.get("event_description"):
            event.event_description = input.get("event_description")
        if input.get("published"):
            event.published = input.get("published")
        if input.get("obligatory"):
            event.obligatory = input.get("obligatory")
        if input.get("starts"):
            event.starts = input.get("starts")
        if input.get("ends"):
            event.ends = input.get("ends")
        if input.get("signup_deadline"):
            event.signup_deadline = input.get("signup_deadline")
        
        event.save()

        return EditEvent(event=event)
    
class DeleteEvent(ClientIDMutation):
    event = Field(lambda: Event)
    class Input:
        eventUid = String()
    
    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = event_models.Event.objects.get(id=uuid.UUID(input["eventUid"]))
        event.delete()
        return DeleteEvent(event=event) # Vad ska returneras?


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
    edit_event = EditEvent.Field()
    delete_event = DeleteEvent.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
