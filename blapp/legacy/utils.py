from django.db import transaction

from blapp.auth import models as auth_models
from blapp.people import models as people_models

from . import models as legacy_models


@transaction.atomic
def import_legacy_data():
    # Imports data from the legacy database.
    # THIS FUNCTION MUST BE IDEMPOTENT, i.e. running it several times should
    # not create any kind of duplicates.

    print('### People and user accounts ###')
    for l_person in legacy_models.Person.objects.all():
        person, person_created = people_models.Person.objects.get_or_create(
            legacy_id=l_person.persid,
        )
        person.first_name = l_person.fnamn
        person.last_name = l_person.enamn
        person.nickname = l_person.smek or ''
        person.email = l_person.epost or None
        person.date_of_birth = l_person.fodd
        person.save()

        if l_person.password:
            user_account, user_account_created = auth_models.UserAccount.objects.get_or_create(
                person=person,
            )
            user_account.username = l_person.blasmail.mailadress
            user_account.password = f'md5$${l_person.password}'
            user_account.save()

        print(person.full_name)
