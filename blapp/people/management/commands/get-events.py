import json
from django.core.management.base import BaseCommand, CommandError
from blapp.legacy.models import Pagang, Arrangemang, Aktivitet

class Command(BaseCommand):
    help = "create json file with legacy id and blapp id for all users"

    def handle(self, *args, **options):
        spelningar = Pagang.objects.all()
        egna_fester = Arrangemang.objects.all()
        andra_aktiviteter = Aktivitet.objects.all()

        data = {"spelningar" : [{"date":str(x.dag), "time":str(x.tid), "fritext" : str(x.fritext), "location" : str(x.plats), } for x in spelningar],
                "egna_fester": [{"event_name" : str(x.arr), "start_date" : str(x.datum), "end_date" : str(x.slutdatum), "fritext" : str(x.fritext)} for x in egna_fester],
                "andra_aktiviteter" : [{"event_name" : str(x.aktivitet), "start_time" : str(x.tid),"end_time" : str(x.sluttid), "location" : str(x.plats)} for x in andra_aktiviteter]
                }
        with open("events.json", "w") as f:
            json.dump(data, f)

