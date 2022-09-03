from importlib.metadata import requires
import uuid
from django.db.models import Q

from graphene import ID, DateTime, Date, Field, Int, ObjectType, Schema, String, Boolean, List
from graphene.relay import Node as RelayNode
from graphene.relay import ClientIDMutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from blapp.auth import models as auth_models
from blapp.commerce import models as commerce_models
from blapp.people import models as people_models
from blapp.shows import models as show_models
from blapp.events import models as event_models


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
            "student_id",
            "date_of_birth",
            "date_of_death",
            "home_address",
            "postal_code",
            "postal_region",
            "country",
            "phone_number",
            "work",
            "arbitrary_text",
            "organ_donor_until",
            "organ_donor",
            "email",
            "legacy_id",
            # Relations
            "purchases",
            "user_account",
            "role_assignments",
        ]
        filter_fields = ["temp_tour18", "id"]


class Role(DjangoObjectType):
    class Meta:
        model = people_models.Role
        interfaces = [Node]
        fields = [
            "id",
            "name",
            "description",
            "membership",
            "engagement",
        ]
        filter_fields = ["name", "membership", "engagement"]


class RoleAssignment(DjangoObjectType):
    class Meta:
        model = people_models.RoleAssignment
        interfaces = [Node]
        fields = [
            "id",
            "start_date_time",
            "end_date_time",
            "trial",
            # Relations
            "role",
            "person",
        ]
        filter_fields = ["id", "person", "role"]


class EditPerson(ClientIDMutation):
    person = Field(lambda: Person)

    class Input:
        uid = String(required=True)
        first_name = String(default=None)
        last_name = String(default=None)
        nickname = String(default=None)
        student_id = String(default=None)
        home_address = String(default=None)
        phone_number = String(default=None)
        work = String(default=None)
        organ_donor = Boolean(default=None)
        organ_donor_until = Date(default=None)
        arbitrary_text = String(default=None)
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
        if input.get("student_id"):
            person.student_id = input["student_id"]
        if input.get("home_address"):
            person.home_address = input["home_address"]
        if input.get("phone_number"):
            person.phone_number = input["phone_number"]
        if input.get("work"):
            person.work = input["work"]
        if input.get("organ_donor") == True or input.get("organ_donor") == False:
            person.organ_donor = input["organ_donor"]
        if input.get("organ_donor_until"):
            person.organ_donor = input["organ_donor_until"]
        if input.get("arbitrary_text"):
            person.arbitrary_text = input["arbitrary_text"]
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
            "published",
            "obligatory",
            "start_date_time",
            "end_date_time",
            "location",
            "responsible_group",
            # Relations
            "attendants",
            # Protected fields
            "contact_person_name",
            "contact_person_email_address",
            "contact_person_phone_number",
            "contact_person_comment",
            "comment",
            "price",
            # Relations
            "creator",
        ]
        filter_fields = {
            "end_date_time": ["exact", "gte", "lte"],
            "start_date_time": ["exact", "gte", "lte"],
            "header": ["icontains", ]
        }


class CreateShow(ClientIDMutation):
    class Input:
        header = String()
        description = String()
        published = Boolean(default=None)
        obligatory = Boolean(default=None)
        start_date_time = DateTime(default=None)
        end_date_time = DateTime(default=None)
        contact_person_name = String(default=None)

    show = Field(lambda: Show)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        show = show_models.Show(
            header=input["header"],
            description=input["description"],
            start_date_time=input["start_date_time"],
            contact_person_name=input["contact_person_name"]
        )
        show.save()
        return CreateShow(show=show)


class EditShow(ClientIDMutation):
    show = Field(lambda: Show)
    creator = Field(lambda: Person)

    class Input:
        showUid = String(required=True)
        creatorUid = String(default=None)
        header = String()
        description = String()
        published = Boolean(default=None)
        obligatory = Boolean(default=None)
        start_date_time = DateTime(default=None)
        end_date_time = DateTime(default=None)
        contact_person_name = String(default=None)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        show = show_models.Show.objects.get(id=uuid.UUID(input["showUid"]))
        if input.get("creatorUid"):
            creator = people_models.Person.objects.get(id=uuid.UUID(input["creatorUid"]))
            show.creator = creator

        if input.get("header"):
            show.header = input.get("header")
        if input.get("description"):
            show.description = input.get("description")
        if input.get("published") != None:
            show.published = input.get("published")
        if input.get("obligatory"):
            show.obligatory = input.get("obligatory")
        if input.get("start_date_time"):
            show.start_date_time = input.get("start_date_time")
        if input.get("end_date_time"):
            show.end_date_time = input.get("end_date_time")
        if input.get("contact_person_name"):
            show.contact_person_name = input.get("contact_person_name")

        show.save()

        return EditShow(show=show)


class Attendance(DjangoObjectType):
    class Meta:
        model = show_models.Attendance
        interfaces = [Node]
        only_fields = [
            "person",
            "show"
        ]
        filter_fields = []


class CreateAttendance(ClientIDMutation):
    show = Field(lambda: Show)
    person = Field(lambda: Person)

    class Input:
        showUid = String(required=True)
        personUid = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        show = show_models.Show.objects.get(id=uuid.UUID(input["showUid"]))
        person = show_models.Person.objects.get(id=uuid.UUID(input["personUid"]))
        try:
            show_models.Attendance.objects.get(show=show, person=person)
            raise Exception("Person already attending.")
        # except eventAttendance.DoesNotExist as exc:
        except event_models.Attendance.DoesNotExist as exc:
            attendance = event_models.Attendance()
            attendance.person = person
            attendance.show = show
            attendance.save()
            return CreateAttendance(person=person, show=show)


class DeleteShow(ClientIDMutation):
    show = Field(lambda: Show)

    class Input:
        showUid = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        show = event_models.Event.objects.get(id=uuid.UUID(input["showUid"]))
        show.delete()
        return DeleteShow(show=show)  # What to return?


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
    people = List(Person, name=String())
    person = Node.Field(Person)
    products = DjangoFilterConnectionField(Product)
    product = Node.Field(Product)
    purchases = DjangoFilterConnectionField(Purchase)
    purchase = Node.Field(Purchase)
    roles = DjangoFilterConnectionField(Role)
    role = Node.Field(Role)
    memberships = List(RoleAssignment, personID=ID(required=True))
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

    def resolve_people(root, info, name):
        if (name):
            print("name: ", name)
            return people_models.Person.objects.filter(
                Q(first_name__icontains=name) |
                Q(nickname__icontains=name) |
                Q(last_name__icontains=name)
            )
        else:
            print("no param")
            return people_models.Person.objects.all()

    def resolve_memberships(root, info, personID):
        print(personID)
        return people_models.RoleAssignment.objects.filter(
            Q(trial=False) & # works
            Q(role__name__icontains = "sax") & # works
            Q(person__first_name = "Abraham") & # works
            Q(person__id = "UGVyc29uOmVkNjdiNGUxLTg1YTAtNDVhNy1hZDRlLTA0NWFmMDA5ZjBkZg==") # not working!
        )


class CoreMutation(ObjectType):
    make_purchase = MakePurchase.Field()
    create_show = CreateShow.Field()
    edit_person = EditPerson.Field()
    edit_show = EditShow.Field()
    delete_show = DeleteShow.Field()
    create_attendance = CreateAttendance.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
