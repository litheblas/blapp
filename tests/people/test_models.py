import pytest
from django.core.exceptions import ValidationError

from blapp.utils.testing import factories

pytestmark = pytest.mark.django_db


class test_person:
    def test_unique_email(self):
        p1 = factories.PersonFactory(email="foo@bar.com")
        p1.full_clean()
        p1.save()

        with pytest.raises(ValidationError):
            p2 = factories.PersonFactory(email="fOo@BAR.com")
            p2.full_clean()
            p2.save()

    def test_non_unique_email(self):
        p1 = factories.PersonFactory(email="")
        p1.full_clean()
        p1.save()
        assert p1
        p2 = factories.PersonFactory(email=None)
        p2.full_clean()
        p2.save()
        assert p2
