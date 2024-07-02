import json
from django.core.management.base import BaseCommand, CommandError

import datetime

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

import blapp.legacy.models as legacy_models







class Command(BaseCommand):
    help = "Saves legacy person in json file"

    def handle(self, *args, **options):
        thing_to_json = {"data" : []}
        legacy_persons = legacy_models.Person.objects.all()
        self.stdout.write("Moving people")
        self.stdout.write("Number of legacy persons: %s" % len(legacy_persons))
        for person in legacy_persons:
            self.stdout.write("Moving person: %s" % person.persid)
            data = {
                'legacyid': person.persid or '',
                'fnamn': person.fnamn or '',
                'enamn': person.enamn or '',
                'smek': person.smek or '',
                'fodd': str(person.fodd) or '',
                'pnr_sista': person.pnr_sista or '',
                'gatuadr': person.gatuadr or '',
                'postnr': person.postnr or '',
                'ort': person.ort or '',
                'land': person.land or '',
                'epost': person.epost or '',
                'studentid': person.studentid or '',
                'hemnr': person.hemnr or '',
                'mobilnr': person.mobilnr or '',
                'jobbnr': person.jobbnr or '',
                'icqnr': person.icqnr or '',
                'fritext': person.fritext or '',
                'gras_medlem_till': str(person.gras_medlem_till) or '',
                'email': person.blasmail.mailadress if person.blasmail else "",
                "username": person.blasmail,
                #'password': person.password or '',
                #'nomail': person.nomail or '',
                #'veg': person.veg or '',
                #'gluten': person.gluten or '',
                #'nykter': person.nykter or '',
                #'allergi': person.allergi or '',
                #'admin': person.admin or '',
                #'sedd_av_anv': person.sedd_av_anv or '',
                #'latlong': person.latlong or '',
                'kon': person.kon or '',
                #'epost_utskick': p
                # erson.epost_utskick or '',
                #'senast_kollad': person.senast_kollad or '',
            }
            thing_to_json['data'].append(data)
        with open("legacy_persons.json", "w") as file:
            self.stdout.write("Writing to file")
            json.dump(thing_to_json, file)
        self.stdout.write("legacy_persons.json Done")



        thing_to_json = {}
        assignments = legacy_models.Funk.objects.all()

        data = {}
        for assignment in assignments:
            self.stdout.write("Moving assignment: %s" % assignment.funkid)
            data[str(assignment.funkid)] = assignment.namn or ''
        thing_to_json['assignments'] = data

        self.stdout.write("Migrating assignment relations")

        assignmentrelations = {}
        all_relations = legacy_models.Persfunk.objects.all()
        for funkid in data.keys():
            certain_rels = all_relations.filter(funk__funkid=funkid)
            done_relations = []
            for rel in certain_rels:
                done_relations.append({"persid": str(rel.pers.persid), "start": str(rel.startdatum), "end": str(rel.slutdatum)})
            assignmentrelations[funkid] = done_relations

        thing_to_json['assignmentrelations'] = assignmentrelations

        self.stdout.write("Migrating instruments")
        instruments = {str(x.instrid) : x.lnamn for x in legacy_models.Instrument.objects.all()}
        thing_to_json['instruments'] = instruments

        all_member_relations = legacy_models.Medlem.objects.all()
        memberrelations = {}
        for instrid in instruments.keys():
            certain_rels = all_member_relations.filter(instr=int(instrid), typ='antagen')
            done_relations = []
            for rel in certain_rels:
                done_relations.append({"persid": str(rel.pers.persid), "start": str(rel.datum)})
            memberrelations[instrid] = done_relations

        gamlingrelations = []
        provrels = []

        for gamlingrel in all_member_relations.filter(typ='gamling'):
            gamlingrelations.append({"persid": str(gamlingrel.pers.persid), "start": str(gamlingrel.datum)})

        memberrelations['gamling'] = gamlingrelations

        for provrel in all_member_relations.filter(typ='prov'):
            provrels.append({"persid": str(provrel.pers.persid), "start": str(provrel.datum)})

        memberrelations['prov'] = provrels

        thing_to_json['memberrelations'] = memberrelations

        with open("legacy_assignments.json", "w") as file:
            self.stdout.write("Writing to file")
            json.dump(thing_to_json, file)








