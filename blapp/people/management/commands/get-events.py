import json
from django.core.management.base import BaseCommand, CommandError
from blapp.people.models import Pagang, Arrangemang, Aktivitet


class Command(BaseCommand):
    help = "create json file with legacy id and blapp id for all users"

    def handle(self, *args, **options):
        spelningar = Pagang.objects.all()
        egna_fester = Arrangemang.objects.all()
        andra_aktiviteter = Aktivitet.objects.all()

        data = {"spelningar" : [{"date":x.dag, "time":x.tid, "fritext" : x.fritext, "location" : x.plats, } for x in spelningar],
                "egna_fester": [{"event_name" : x.arr, "start_date" : x.datum, "end_date" : x.slutdatum, "fritext" : x.fritext} for x in egna_fester],
                "andra_aktiviteter" : [{"event_name" : x.aktivitet, "start_time" : x.tid,"end_time" : x.sluttid, "location" : x.plats} for x in andra_aktiviteter]
                }
        with open("events.json", "w") as f:
            json.dump(data, f)

