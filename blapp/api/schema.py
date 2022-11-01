import uuid

from graphene import ID, DateTime, Date, Field, Int, ObjectType, Schema, String
from graphene.relay import Node as RelayNode
from graphene.relay import ClientIDMutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from blapp.auth import models as auth_models
from blapp.commerce import models as commerce_models
from blapp.people import models as people_models
from blapp.shows import models as show_models
from blapp.events import models as event_models

from . import filters


def check_staff_superuser_person(info, self):
    return info.context.user.is_staff or info.context.user.is_superuser or info.context.user.person == self

def check_superuser_person(info, self):
    return info.context.user.is_superuser or info.context.user.person == self

def check_staff_superuser(info):
    return info.context.user.is_staff or info.context.user.is_superuser

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

class PhoneNumber(DjangoObjectType):
    class Meta:
        model = people_models.PhoneNumber
        interfaces = [Node]
        fields = [
            "id",
            "person",
            "label",
            "phone_number"
        ]
        filter_fields = ["person"]
    

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
            "street_address",
            "postal_code",
            "postal_region",
            "country",
            "national_id_number",
            "dietary_preferences",
            "arbitrary_text",
            # Relations
            "purchases",
            "user_account",
            "phone_numbers",
        ]
        filterset_class = filters.PersonFilter

    def resolve_national_id_number(self, info):
        if check_staff_superuser_person(info, self):
            return self.national_id_number
        return ""

    def resolve_dietary_preferences(self, info):
        if check_staff_superuser_person(info, self):
            return self.dietary_preferences
        return ""

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
        filter_fields = ["person", "role", "role__membership", "role__engagement"]

class Event(DjangoObjectType):
    class Meta:
        model = event_models.Event
        interfaces = [Node]
        fields = [
            "header",
            "description",
            "location",
            "start_date_time",
            "end_date_time",
        ]
        filter_fields = {
            "end_date_time": ["exact", "gte", "lte"],
            "start_date_time": ["exact", "gte", "lte"],
            "header": ["icontains", ]
        }

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
            "contact_person_comment",
            "comment",
            "fee",
        ]
        filter_fields = {
            "end_date_time": ["exact", "gte", "lte"],
            "start_date_time": ["exact", "gte", "lte"],
            "header": ["icontains", ]
        }

    def resolve_contact_person_name(self, info):
        if check_staff_superuser(info):
            return self.contact_person_name
        return ""
    
    def resolve_contact_person_email_address(self, info):
        if check_staff_superuser(info):
            return self.contact_person_email_address
        return ""
    
    def resolve_contact_person_phone_number(self, info):
        if check_staff_superuser(info):
            return self.contact_person_phone_number
        return ""
    
    def resolve_contact_person_comment(self, info):
        if check_staff_superuser(info):
            return self.contact_person_comment
        return ""
    
    def resolve_comment(self, info):
        if check_staff_superuser(info):
            return self.comment
        return ""
    
    def resolve_fee(self, info):
        if check_staff_superuser(info):
            return self.fee
        return ""

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
        street_address = String(default=None)
        postal_code = String(default=None)
        postal_region = String(default=None)
        country = String(default=None)
        national_id_number = String(default=None)
        student_id = String(default=None)
        dietary_preferences = String(default=None)
        arbitrary_text = String(default=None)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        person = Node.get_node_from_global_id(info, input["uid"])
        if check_superuser_person(info, person):
            if first_name := input.get("first_name"):
                person.first_name = first_name
            if last_name := input.get("last_name"):
                person.last_name = last_name
            if nickname := input.get("nickname"):
                person.nickname = nickname
            if date_of_birth := input.get("date_of_birth"):
                person.date_of_birth = date_of_birth
            if date_of_death := input.get("date_of_death"):
                person.date_of_death = date_of_death
            if email := input.get("email"):
                person.email = email
            if street_address := input.get("street_address"):
                person.street_address = street_address
            if postal_region := input.get("postal_region"):
                person.postal_region = postal_region
            if postal_code := input.get("postal_code"):
                person.postal_code = postal_code
            if country := input.get("country"):
                person.country = country
            if national_id_number := input.get("national_id_number"):
                person.national_id_number = national_id_number
            if student_id := input.get("student_id"):
                person.student_id = student_id
            if dietary_preferences := input.get("dietary_preferences"):
                person.dietary_preferences = dietary_preferences
            if arbitrary_text := input.get("arbitrary_text"):
                person.arbitrary_text = arbitrary_text
            person.save()
        return EditPerson(person=person)

class CoreQuery:
    people = DjangoFilterConnectionField(Person)
    person = Node.Field(Person)
    products = DjangoFilterConnectionField(Product)
    product = Node.Field(Product)
    phone_numbers = DjangoFilterConnectionField(PhoneNumber)
    phone_number = Node.Field(PhoneNumber)
    purchases = DjangoFilterConnectionField(Purchase)
    purchase = Node.Field(Purchase)
    roles = DjangoFilterConnectionField(Role)
    role = Node.Field(Role)
    role_assignments = DjangoFilterConnectionField(RoleAssignment)
    role_assignment = Node.Field(RoleAssignment)
    events = DjangoFilterConnectionField(Event)
    event = Node.Field(Event)
    shows = DjangoFilterConnectionField(Show)
    show = Node.Field(Show)
    sale_points = DjangoFilterConnectionField(SalePoint)
    sale_point = Node.Field(SalePoint)
    user_accounts = DjangoFilterConnectionField(UserAccount)
    user_account = Node.Field(UserAccount)


class CoreMutation(ObjectType):
    make_purchase = MakePurchase.Field()
    edit_person = EditPerson.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
