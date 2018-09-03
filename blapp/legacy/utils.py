from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import transaction

from blapp.auth import models as auth_models
from blapp.people import models as people_models

from . import models as legacy_models

email_validator = EmailValidator()


@transaction.atomic
def import_legacy_data():
    # Imports data from the legacy database.
    # THIS FUNCTION MUST BE IDEMPOTENT, i.e. running it several times should
    # not create any kind of duplicates.

    print("### People and user accounts ###")
    for l_person in legacy_models.Person.objects.all().order_by("fnamn"):
        person, person_created = people_models.Person.objects.get_or_create(
            legacy_id=l_person.persid
        )
        person.first_name = l_person.fnamn.strip()
        person.last_name = l_person.enamn.strip()
        person.nickname = l_person.smek.strip() if l_person.smek else ""
        try:
            email_validator(l_person.epost)
            person.email = l_person.epost
        except ValidationError:
            person.email = None
        person.date_of_birth = l_person.fodd

        person.clean_fields(exclude=["first_name", "last_name"])
        person.save()

        if person.email and l_person.password:
            user_account, user_account_created = auth_models.UserAccount.objects.get_or_create(
                person=person
            )
            user_account.username = l_person.blasmail.mailadress.strip().lower()
            user_account.password = f"md5$${l_person.password}"
            user_account.save()

        print(person.full_name)
