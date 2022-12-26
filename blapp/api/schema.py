import uuid

from graphene import (
    ID,
    Boolean,
    Date,
    DateTime,
    Field,
    Int,
    ObjectType,
    Schema,
    String,
)
from graphene.relay import ClientIDMutation
from graphene.relay import Node as RelayNode
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

from blapp.auth import models as auth_models
from blapp.commerce import models as commerce_models
from blapp.events import models as event_models
from blapp.people import models as people_models
from blapp.shows import models as show_models

from . import filters


def check_staff_superuser_person(info, self):
    return (
        info.context.user.is_staff
        or info.context.user.is_superuser
        or info.context.user.person == self
    )


def check_person(info, self):
    return info.context.user.person == self


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
            "phone_number_1",
            "phone_number_1_label",
            "phone_number_2",
            "phone_number_2_label",
            "phone_number_3",
            "phone_number_3_label",
            # Relations
            "purchases",
            "user_account",
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
            "owner",
            "header",
            "description",
            "location",
            "start_date_time",
            "end_date_time",
        ]
        filter_fields = {
            "end_date_time": ["exact", "gte", "lte"],
            "start_date_time": ["exact", "gte", "lte"],
            "header": [
                "icontains",
            ],
        }


class Attendance(DjangoObjectType):
    class Meta:
        model = event_models.Attendance
        interfaces = [Node]
        fields = [
            "id",
            "event",
            "person",
        ]
        filter_fields = [
            "person",
            "event",
        ]


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
            "header": [
                "icontains",
            ],
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


class CreatePerson(ClientIDMutation):
    person = Field(lambda: Person)

    class Input:
        # UserAccount parameters
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        first_name = String(required=True)
        last_name = String(required=True)

        # Person parameters
        nickname = String(blank=True)
        date_of_birth = Date(null=True)
        street_address = String(blank=True)
        postal_code = String(blank=True)
        postal_region = String(blank=True)
        country = String(blank=True)
        national_id_number = String(blank=True)
        student_id = String(blank=True)
        dietary_preferences = String(blank=True)
        arbitrary_text = String(blank=True)
        phone_number_1 = String(blank=True)
        phone_number_1_label = String(blank=True)
        phone_number_2 = String(blank=True)
        phone_number_2_label = String(blank=True)
        phone_number_3 = String(blank=True)
        phone_number_3_label = String(blank=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if check_staff_superuser(info):
            useraccount = auth_models.UserAccount.objects.create_user(
                username=input["username"],
                email=input["email"],
                password=input["password"],
                first_name=input["first_name"],
                last_name=input["last_name"],
            )
            useraccount.save()

            if nickname := input.get("nickname"):
                useraccount.person.nickname = nickname
            if date_of_birth := input.get("date_of_birth"):
                useraccount.person.date_of_birth = date_of_birth
            if street_address := input.get("street_address"):
                useraccount.person.street_address = street_address
            if postal_code := input.get("postal_code"):
                useraccount.person.postal_code = postal_code
            if postal_region := input.get("postal_region"):
                useraccount.person.postal_region = postal_region
            if country := input.get("country"):
                useraccount.person.country = country
            if national_id_number := input.get("national_id_number"):
                useraccount.person.national_id_number = national_id_number
            if student_id := input.get("student_id"):
                useraccount.person.student_id = student_id
            if dietary_preferences := input.get("dietary_preferences"):
                useraccount.person.dietary_preferences = dietary_preferences
            if arbitrary_text := input.get("arbitrary_text"):
                useraccount.person.arbitrary_text = arbitrary_text
            if phone_number_1 := input.get("phone_number_1"):
                useraccount.person.phone_number_1 = phone_number_1
            if phone_number_1_label := input.get("phone_number_1_label"):
                useraccount.person.phone_number_1_label = phone_number_1_label
            if phone_number_2 := input.get("phone_number_2"):
                useraccount.person.phone_number_2 = phone_number_2
            if phone_number_2_label := input.get("phone_number_2_label"):
                useraccount.person.phone_number_2_label = phone_number_2_label
            if phone_number_3 := input.get("phone_number_3"):
                useraccount.person.phone_number_3 = phone_number_3
            if phone_number_3_label := input.get("phone_number_3_label"):
                useraccount.person.phone_number_3_label = phone_number_3_label
            useraccount.person.save()
            return CreatePerson(person=useraccount.person)
        return GraphQLError("Unauthorized action.")


class EditPerson(ClientIDMutation):
    person = Field(lambda: Person)

    class Input:
        uid = String(required=True)
        first_name = String(blank=True)
        last_name = String(blank=True)
        nickname = String(blank=True)

        date_of_birth = Date(null=True)
        date_of_death = Date(null=True)

        email = String(blank=True)
        street_address = String(blank=True)
        postal_code = String(blank=True)
        postal_region = String(blank=True)
        country = String(blank=True)
        national_id_number = String(blank=True)
        student_id = String(blank=True)
        dietary_preferences = String(blank=True)
        arbitrary_text = String(blank=True)

        phone_number_1 = String(blank=True)
        phone_number_1_label = String(blank=True)
        phone_number_2 = String(blank=True)
        phone_number_2_label = String(blank=True)
        phone_number_3 = String(blank=True)
        phone_number_3_label = String(blank=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        person = Node.get_node_from_global_id(info, input["uid"])
        if check_person(info, person):
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
            if phone_number_1 := input.get("phone_number_1"):
                person.phone_number_1 = phone_number_1
            if phone_number_1_label := input.get("phone_number_1_label"):
                person.phone_number_1_label = phone_number_1_label
            if phone_number_2 := input.get("phone_number_2"):
                person.phone_number_2 = phone_number_2
            if phone_number_2_label := input.get("phone_number_2_label"):
                person.phone_number_2_label = phone_number_2_label
            if phone_number_3 := input.get("phone_number_3"):
                person.phone_number_3 = phone_number_3
            if phone_number_3_label := input.get("phone_number_3_label"):
                person.phone_number_3_label = phone_number_3_label
            person.save()
        return EditPerson(person=person)


class CreateEvent(ClientIDMutation):
    event = Field(lambda: Event)

    class Input:
        header = String(required=True)
        description = String(blank=True)
        location = String(blank=True)
        start_date_time = DateTime(required=True)
        end_date_time = DateTime(required=True)

    @classmethod
    def mutate_and_get_payload(clf, root, info, **input):
        event = event_models.Event()
        event.owner = info.context.user.person
        event.header = input.get("header")
        if description := input.get("description"):
            event.description = description
        if location := input.get("location"):
            event.location = location
        event.start_date_time = input.get("start_date_time")
        event.end_date_time = input.get("end_date_time")
        event.save()
        return CreateEvent(event=event)


class EditEvent(ClientIDMutation):
    event = Field(lambda: Event)

    class Input:
        uid = String(required=True)
        header = String(blank=True)
        description = String(blank=True)
        location = String(blank=True)
        start_date_time = DateTime(null=True)
        end_date_time = DateTime(null=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = Node.get_node_from_global_id(info, input.get("uid"))
        if check_person(info, event.owner):
            if header := input.get("header"):
                event.header = header
            if description := input.get("description"):
                event.description = description
            if location := input.get("location"):
                event.location = location
            if start_date_time := input.get("start_date_time"):
                event.start_date_time = start_date_time
            if end_date_time := input.get("end_date_time"):
                event.end_date_time = end_date_time
            event.save()
        return EditEvent(event=event)


class DeleteEvent(ClientIDMutation):
    event = Field(lambda: Event)

    class Input:
        uid = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = Node.get_node_from_global_id(info, input.get("uid"))
        if check_person(info, event.owner):
            event.delete()
        return DeleteEvent(event=event)


class EventSignup(ClientIDMutation):
    ok = Boolean()

    class Input:
        event_uid = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        attendance, created = event_models.Attendance.objects.get_or_create(
            person=info.context.user.person,
            event=Node.get_node_from_global_id(info, input.get("event_uid")),
        )
        if not created:
            return GraphQLError(
                'You are already signed up to event "{}".'.format(
                    attendance.event.header,
                ),
            )
        return EventSignup(ok=True)


class EventQuit(ClientIDMutation):
    ok = Boolean()

    class Input:
        event_uid = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = Node.get_node_from_global_id(info, input.get("event_uid"))
        try:
            event_models.Attendance.objects.get(
                person=info.context.user.person,
                event=event,
            ).delete()
            return EventQuit(ok=True)
        except event_models.Event.DoesNotExist:
            return GraphQLError(
                'You are not registered to event "{}".'.format(event.header),
            )


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
    events = DjangoFilterConnectionField(Event)
    event = Node.Field(Event)
    attendances = DjangoFilterConnectionField(Attendance)
    attendance = Node.Field(Attendance)
    shows = DjangoFilterConnectionField(Show)
    show = Node.Field(Show)
    sale_points = DjangoFilterConnectionField(SalePoint)
    sale_point = Node.Field(SalePoint)
    user_accounts = DjangoFilterConnectionField(UserAccount)
    user_account = Node.Field(UserAccount)


class CoreMutation(ObjectType):
    make_purchase = MakePurchase.Field()
    create_person = CreatePerson.Field()
    edit_person = EditPerson.Field()
    create_event = CreateEvent.Field()
    edit_event = EditEvent.Field()
    delete_event = DeleteEvent.Field()
    event_signup = EventSignup.Field()
    event_quit = EventQuit.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
