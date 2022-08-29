import uuid

from graphene import ID, DateTime, Field, Int, ObjectType, Schema, String
from graphene.relay import Node as RelayNode
from graphene.relay import ClientIDMutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from blapp.auth import models as auth_models
from blapp.commerce import models as commerce_models
from blapp.people import models as people_models
from blapp.shows import models as show_models


class Node(RelayNode):
    pass


class UserAccount(DjangoObjectType):
    class Meta:
        model = auth_models.UserAccount
        interfaces = [Node]
        fields = [
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
        fields = ["id", "name", "description", "price"]
        filter_fields = []


class SalePoint(DjangoObjectType):
    class Meta:
        model = commerce_models.SalePoint
        interfaces = [Node]
        fields = ["id", "name", "description"]
        filter_fields = []


class Purchase(DjangoObjectType):
    class Meta:
        model = commerce_models.Purchase
        interfaces = [Node]
        fields = [
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
        fields = [
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

class Role(DjangoObjectType):
    class Meta:
        model = people_models.Role
        interfaces = [Node]
        fields = [
            "id",
            "name",
            "description",
        ]
        filter_fields = ["membership", "engagement"]

class RoleAssignment(DjangoObjectType):
    class Meta:
        model = people_models.RoleAssignment
        interfaces = [Node]
        fields = [
            "id",
            "period",
            "trial",
            # Relations
            "role",
            "person",
        ]
        filter_fields = ["person", "role"]

class Show(DjangoObjectType):
    class Meta:
        model = show_models.Show
        interfaces = [Node]
        fields = [
            "id",
            "header",
            "description",
            "start_date_time",
            "end_date_time",
            "location",
            "driving_section",
            # Protected fields
            "contact_person_name",
            "contact_person_email_address",
            "contact_person_phone_number",
            "fee",
        ]
        filter_fields = {
            "end_date_time": ["exact", "gte", "lte"],
            "start_date_time": ["exact", "gte", "lte"],
            "header": ["icontains", ]
        }

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


class CoreQuery:
    people = DjangoFilterConnectionField(Person)
    person = Node.Field(Person)
    products = DjangoFilterConnectionField(Product)
    product = Node.Field(Product)
    purchases = DjangoFilterConnectionField(Purchase)
    purchase = Node.Field(Purchase)
    roles = DjangoFilterConnectionField(Role)
    role = Node.Field(Role)
    role_assignments = DjangoFilterConnectionField(RoleAssignment)
    role_assignment = Node.Field(RoleAssignment)
    shows = DjangoFilterConnectionField(Show)
    show = Node.Field(Show)
    sale_points = DjangoFilterConnectionField(SalePoint)
    sale_point = Node.Field(SalePoint)
    user_accounts = DjangoFilterConnectionField(UserAccount)
    user_account = Node.Field(UserAccount)


class CoreMutation(ObjectType):
    make_purchase = MakePurchase.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
