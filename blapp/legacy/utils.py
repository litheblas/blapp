import datetime

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.db import transaction
from psycopg2.extras import DateRange

from blapp.auth import models as auth_models
from blapp.people import models as people_models

from . import models as legacy_models

INF_DATE = datetime.date(9999, 12, 31)

email_validator = EmailValidator()


def _medlem_role_assignments(person, l_person):
    open_assignment = None

    for l_medlem in legacy_models.Medlem.objects.filter(pers=l_person.persid).order_by(
        "datum",
    ):
        # print(
        #     l_medlem.datum,
        #     ":",
        #     l_medlem.typ,
        #     legacy_models.Instrument.objects.get(instrid=l_medlem.instr).lnamn
        #     if l_medlem.instr
        #     else "",
        # )
        if open_assignment and (l_medlem.typ == "gamling" or l_medlem.typ == "antagen"):
            open_assignment.legacy_end_id = l_medlem.medlemid
            if l_medlem.datum != INF_DATE:
                open_assignment.period._upper = l_medlem.datum
            open_assignment.save()
            open_assignment = None

            if l_medlem.typ == "gamling":
                continue

        (
            assignment,
            assignment_created,
        ) = people_models.RoleAssignment.objects.get_or_create(
            legacy_table=legacy_models.Medlem._meta.db_table,
            legacy_start_id=l_medlem.medlemid,
            defaults=dict(
                person=person,
                role=people_models.Role.objects.get(
                    legacy_table=legacy_models.Instrument._meta.db_table,
                    legacy_id={"gamling": "okänt", "heder": "heder"}.get(
                        l_medlem.typ,
                        l_medlem.instr,
                    ),
                ),
                period=DateRange(l_medlem.datum, None),
                trial=True if l_medlem.typ == "prov" else False,
            ),
        )

        if not l_medlem.typ == "gamling":
            open_assignment = assignment

    # for ass in person.role_assignments.all():
    #     print(ass.period.lower, "–", ass.period.upper, ":", ass.role.name, ass.trial)


def _persfunk_role_assignments(person, l_person):
    for l_persfunk in legacy_models.Persfunk.objects.filter(pers=l_person):
        (
            assignment,
            assignment_created,
        ) = people_models.RoleAssignment.objects.get_or_create(
            legacy_table=legacy_models.Persfunk._meta.db_table,
            legacy_start_id=l_persfunk.id,
            legacy_end_id=l_persfunk.id,
            defaults=dict(
                person=person,
                role=people_models.Role.objects.get(
                    legacy_table=legacy_models.Funk._meta.db_table,
                    legacy_id=l_persfunk.funk_id,
                ),
                period=DateRange(
                    l_persfunk.startdatum,
                    l_persfunk.slutdatum if l_persfunk.slutdatum != INF_DATE else None,
                ),
                trial=False,
            ),
        )


def _roles():
    funcs_role, funcs_role_created = people_models.Role.objects.get_or_create(
        legacy_table=legacy_models.Funk._meta.db_table,
        legacy_id="",
        defaults=dict(name="Förtroende- och funktionärsposter"),
    )
    for l_funk in legacy_models.Funk.objects.all():
        func_role, func_role_created = people_models.Role.objects.get_or_create(
            legacy_table=legacy_models.Funk._meta.db_table,
            legacy_id=l_funk.funkid,
            defaults=dict(
                name=l_funk.namn.strip(),
                description=l_funk.beskr.strip(),
                parent=funcs_role,
                engagement=True,
            ),
        )

        print(funcs_role.name, "/", func_role.name)

    (
        section_and_instruments_role,
        section_and_instruments_role_created,
    ) = people_models.Role.objects.get_or_create(
        legacy_table=legacy_models.Sektion._meta.db_table,
        legacy_id="",
        defaults=dict(name="Sektioner och instrument"),
    )
    for l_sektion in legacy_models.Sektion.objects.all():
        section_role, section_role_created = people_models.Role.objects.get_or_create(
            legacy_table=legacy_models.Sektion._meta.db_table,
            legacy_id=l_sektion.sektid,
            defaults=dict(
                name=l_sektion.lnamn.strip(),
                parent=section_and_instruments_role,
            ),
        )

        for l_instrument in legacy_models.Instrument.objects.filter(
            sekt=l_sektion.sektid,
        ):
            (
                instrument_role,
                instrument_role_created,
            ) = people_models.Role.objects.get_or_create(
                legacy_table=legacy_models.Instrument._meta.db_table,
                legacy_id=l_instrument.instrid,
                defaults=dict(
                    parent=section_role,
                    name=l_instrument.lnamn.strip(),
                    membership=True,
                ),
            )

            print(section_role.name, "/", instrument_role.name)

    (
        unknown_instrument_role,
        unknown_instrument_role_created,
    ) = people_models.Role.objects.get_or_create(
        legacy_table=legacy_models.Instrument._meta.db_table,
        legacy_id="okänt",
        defaults=dict(name="[okänt instrument]", membership=True),
    )

    honorary_role, honorary_role_created = people_models.Role.objects.get_or_create(
        legacy_table=legacy_models.Instrument._meta.db_table,
        legacy_id="heder",
        defaults=dict(name="Hedersmedlem", parent=funcs_role, membership=True),
    )


@transaction.atomic
def import_legacy_data():
    # Imports data from the legacy database.
    # THIS FUNCTION MUST BE IDEMPOTENT, i.e. running it several times should
    # not create any kind of duplicates or remove anything without legacy IDs.
    # If there is a conflict, the non-legacy data should probably have
    # precedence.

    print("### Roles ###")
    _roles()

    print("### People and user accounts ###")
    for l_person in legacy_models.Person.objects.all().order_by("fnamn"):
        person, person_created = people_models.Person.objects.get_or_create(
            legacy_id=l_person.persid,
        )
        person.first_name = l_person.fnamn.strip()
        person.last_name = l_person.enamn.strip()
        person.nickname = l_person.smek.strip() if l_person.smek else ""
        try:
            email_validator(l_person.epost)
            person.email = l_person.epost.strip()
        except ValidationError:
            person.email = None
        person.date_of_birth = l_person.fodd

        person.clean_fields(exclude=["first_name", "last_name"])
        person.save()

        if person.email and l_person.password:
            (
                user_account,
                user_account_created,
            ) = auth_models.UserAccount.objects.get_or_create(person=person)
            user_account.username = l_person.blasmail.mailadress.strip().lower()
            user_account.password = f"md5$${l_person.password}"
            user_account.save()

        print(person.full_name)

        _medlem_role_assignments(person, l_person)
        _persfunk_role_assignments(person, l_person)
