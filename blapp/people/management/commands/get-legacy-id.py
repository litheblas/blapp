import json
from django.core.management.base import BaseCommand, CommandError
from blapp.people.models import Person
from blapp.auth.models import UserAccount

class Command(BaseCommand):
    help = "create json file with legacy id and blapp id for all users"

    def handle(self, *args, **options):
        persons = Person.objects.all()
        useraccounts = UserAccount.objects.all()
        data = {}
        for person in persons:
            this_account = useraccounts.get(person=person)
            if this_account:
                data[str(person.legacy_id)] = str(this_account.id)
            else:
                data[str(person.legacy_id)] = str(person.id)
        with open("legacy_id_to_blapp_id.json", "w") as f:
            json.dump(data, f)
        data = {}
        for person in persons:
            data[str(person.id)] = str(person.legacy_id)
        with open("blapp_id_to_legacy_id.json", "w") as f:
            json.dump(data, f)



