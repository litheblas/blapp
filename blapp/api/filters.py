from django.db.models import CharField
from django.db.models import Value as V
from django.db.models.functions import Concat
from django_filters import CharFilter, FilterSet

from blapp.people import models as people_models


class PersonFilter(FilterSet):
    full_name = CharFilter(method="full_name_filter")

    class Meta:
        model = people_models.Person
        fields = ["temp_tour18", "full_name"]

    def full_name_filter(self, queryset, name, value):
        query = people_models.Person.objects.annotate(
            conc=Concat(
                "first_name",
                V(" "),
                "nickname",
                V(" "),
                "last_name",
                output_field=CharField(),
            ),
        )
        for word in value.split():
            query = query.filter(conc__icontains=word)
        return query
