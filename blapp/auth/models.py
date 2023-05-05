from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from blapp.people.models import Person
from blapp.utils.db_fields import (
    DescriptionField,
    NameField,
    PrimaryKeyUUIDField,
)
from blapp.utils.random import hex_string

from .constants import AUTH_TOKEN_LENGTH


class UserAccountManager(BaseUserManager):
    def create_user(
        self,
        username=None,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
    ):
        if not username:
            raise ValueError("Users must have a username")
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        assert not UserAccount.objects.filter(username=username).exists()

        person = Person.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        user = self.model(username=username, person=person)
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.create_user(*args, **kwargs)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin, models.Model):
    id = PrimaryKeyUUIDField()

    person = models.OneToOneField(
        "people.Person",
        related_name="user_account",
        on_delete=models.CASCADE,
        verbose_name=_("person"),
    )

    username = models.CharField(
        max_length=256,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        verbose_name=_("username"),
    )

    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("is staff"))

    objects = UserAccountManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["person"]

    def __str__(self):
        return str(self.person)

    def save(self, *args, **kwargs):
        assert self.person.email
        super().save(*args, **kwargs)

    @property
    def email(self):
        # Having this available on the user model makes some third-party apps
        # less sad.
        return self.person.email

    def get_username(self):
        return self.username

    def get_full_name(self):
        return self.person.full_name

    def get_short_name(self):
        return self.person.short_name


class ServiceAccount(models.Model):
    id = PrimaryKeyUUIDField()

    token = models.CharField(max_length=AUTH_TOKEN_LENGTH, editable=False)

    name = NameField()
    description = DescriptionField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = hex_string(length=AUTH_TOKEN_LENGTH)
        super().save(*args, **kwargs)

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True
