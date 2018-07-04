import pytest
from django.core.exceptions import ValidationError

from blapp.utils.testing import factories

pytestmark = pytest.mark.django_db


class test_person:
    def test_unique_email(self):
        factories.PersonFactory.create(email="foo@bar.com")

        with pytest.raises(ValidationError):
            factories.PersonFactory.create(email="fOo@BAR.com")

    def test_non_unique_email(self):
        assert factories.PersonFactory.create(email="")
        assert factories.PersonFactory.create(email=None)
