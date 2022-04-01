from email.policy import default
from unittest import skip
import uuid

from graphene import ID, DateTime, Date, Field, Int, ObjectType, Schema, String, Boolean, List
from graphene.relay import Node as RelayNode
from graphene.relay import ClientIDMutation
from graphene.types import interface
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from django.db.models import Q
import django_filters

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
            "event",
        ]
        filter_fields = ["person"]


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
            "home_address",
            "phone_number",
            "email",
            "student_id",
            "workplace",
            "organ_donor",
            "organ_donor_until",
            "arbitrary_text",
            "date_of_birth",
            "date_of_death",
            "legacy_id",
            # Relations
            "purchases",
            "user_account",
        ]
        filter_fields = ["temp_tour18", "id", "first_name", "nickname", "last_name"]

class PeopleFilter(django_filters.FilterSet):
    people = List(Person, search=String())

    def resolve_people(parent, info, search):
        if search:
            filter = (
                Q(first_name__icontains=search)
                | Q(nickname__icontains=search)
                | Q(last_name__icontains=search)
            )
            return people_models.Person.objects.filter(filter)
        
        return people_models.Person.objects.all()



class EditPerson(ClientIDMutation):
    person = Field(lambda: Person)
    
    class Input:
        uid = String(required=True)
        first_name = String(default=None)
        last_name = String(default=None)
        nickname = String(default=None)
        home_address = String(default=None)
        phone_number = String(default=None)
        student_id = String(default=None)
        workplace = String(default=None)
        organ_donor_until = String(default=None)
        organ_donor = Boolean(default=None)
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
        if input.get("phone_number"):
            person.phone_number = input["phone_number"]
        if input.get("student_id"):
            person.student_id = input["student_id"]
        if input.get("workplace"):
            person.workplace = input["workplace"]
        if input.get("arbitrary_text"):
            person.arbitrary_text = input["arbitrary_text"]
        if input.get("home_address"):
            person.home_address = input["home_address"]
        if input.get("organ_donor") == True or input.get("organ_donor") == False:
            person.organ_donor = input["organ_donor"]
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
            "contact_person",
            "contact_mail",
            "contact_phone",
            "rating",
            "price",
            "comment",
            # Relations
            "creator",
            "attendants"
        ]
        filter_fields = []

class CreateEvent(ClientIDMutation):
    class Input:
        event_name = String(required=True)
        event_description = String(required=True)
        published = Boolean(required=True, default=False)
        obligatory = Boolean(default=False)
        starts = DateTime(required=True, default=None)
        ends = DateTime(default=None)
        signup_deadline = DateTime(default=None)
        contact_person = String(default=None)
        contact_mail = String(default=None)
        contact_phone = String(default=None)
        rating = String(default=None)
        price = String(default=None)
        comment = String(default=None)
    
    event = Field(lambda: Event)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        
        if not input.get("obligatory"):
            obligatory = False
        else:
            obligatory = input["obligatory"]

        if not input.get("ends"):
            ends = "2022-01-22T07:44:53+03:00"
        else:
            ends = input["ends"]

        if not input.get("signup_deadline"):
            signup_deadline = "2022-01-22T07:44:53+03:00"
        else:
            signup_deadline = input["signup_deadline"]

        if not input.get("contact_person"):
            contact_person = ""
        else:
            contact_person = input["contact_person"]

        if not input.get("contact_mail"):
            contact_mail = ""
        else:
            contact_mail = input["contact_mail"]

        if not input.get("contact_phone"):
            contact_phone = ""
        else:
            contact_phone = input["contact_phone"]

        if not input.get("rating"):
            rating = ""
        else:
            rating = input["rating"]

        if not input.get("price"):
            price = ""
        else:
            price = input["price"]

        if not input.get("comment"):
            comment = ""
        else:
            comment = input["comment"]

        event = event_models.Event(
            event_name=input["event_name"],
            event_description=input["event_description"],
            published=input["published"],
            starts=input["starts"],
            obligatory=obligatory,
            ends=ends,
            signup_deadline=signup_deadline,
            contact_person=contact_person,
            contact_mail=contact_mail,
            contact_phone=contact_phone,
            rating=rating,
            price=price,
            comment=comment,
            )
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
        contact_person = String(default=None)
        contact_mail = String(default=None)
        contact_phone = String(default=None)
        rating = String(default=None)
        price = String(default=None)
        comment = String(default=None)

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
        if input.get("published") != None:
            event.published = input.get("published")
        if input.get("obligatory"):
            event.obligatory = input.get("obligatory")
        if input.get("starts"):
            event.starts = input.get("starts")
        if input.get("ends"):
            event.ends = input.get("ends")
        if input.get("signup_deadline"):
            event.signup_deadline = input.get("signup_deadline")
        if input.get("contact_person"):
            event.contact_person = input.get("contact_person")
        if input.get("contact_mail"):
            event.contact_mail = input.get("contact_mail")
        if input.get("contact_phone"):
            event.contact_phone = input.get("contact_phone")
        if input.get("rating"):
            event.rating = input.get("rating")
        if input.get("price"):
            event.price = input.get("price")
        if input.get("comment"):
            event.comment = input.get("comment")
        
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

class Attendance(DjangoObjectType):
    class Meta:
        model = event_models.Attendance
        interfaces = [Node]
        only_fields = [
            "person",
            "event"
        ]
        filter_fields = []

class CreateAttendance(ClientIDMutation):
    event = Field(lambda: Event)
    person = Field(lambda: Person)

    class Input:
        eventUid = String(required=True)
        personUid = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        event = event_models.Event.objects.get(id=uuid.UUID(input["eventUid"]))
        person = event_models.Person.objects.get(id=uuid.UUID(input["personUid"]))
        try:
            event_models.Attendance.objects.get(event=event, person=person)
            raise Exception("Unique constraint not satisfied.")
        #except eventAttendance.DoesNotExist as exc:
        except event_models.Attendance.DoesNotExist as exc:
            attendance = event_models.Attendance()
            attendance.person = person
            attendance.event = event
            attendance.save()
            return CreateAttendance(person=person, event=event)

class CoreQuery:
    people = DjangoFilterConnectionField(Person, search = String())

    def resolve_people(self, info, search=None):
        if search:
            filter = (
                Q(first_name__icontains=search)
                | Q(nickname__icontains=search)
                | Q(last_name__icontains=search)
            )
            return people_models.Person.objects.filter(filter)
        
        return people_models.Person.objects.all()
        
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
    attendances = DjangoFilterConnectionField(Attendance)
    attendance = Node.Field(Event)


class CoreMutation(ObjectType):
    make_purchase = MakePurchase.Field()
    create_event = CreateEvent.Field()
    edit_person = EditPerson.Field()
    edit_event = EditEvent.Field()
    delete_event = DeleteEvent.Field()
    create_attendance = CreateAttendance.Field()


class QuerySchema(CoreQuery, ObjectType):
    # Required by the Relay spec
    node = Node.Field()


schema = Schema(query=QuerySchema, mutation=CoreMutation)
