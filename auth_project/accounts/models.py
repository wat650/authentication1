import uuid
from base64 import urlsafe_b64encode

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import ActivatorModel, TimeStampedModel


from accounts.manager import UserManager
from utils.enums import GenderChoices


class BaseModel(TimeStampedModel, ActivatorModel):
    """
    Name: BaseModel

    Description: This class help to generate an uuid pk for all models means that all
                 the project's models should inherit from this model.

    Author: angewatiopiankeu@gmail.com
    """

    id = models.UUIDField(
        default=uuid.uuid4, null=False, blank=False, unique=True, primary_key=True
    )
    is_deleted = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, null=True, blank=True)
    author = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    is_client = models.BooleanField(_('client status'), default=True)
    is_admin = models.BooleanField(_('admin status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.last_name, self.first_name)
        return full_name.strip()

    @property
    def url_safe_b64_encoded_id(self) -> str:
        """Encode the user id as a b64 url safe string."""

        return urlsafe_b64encode(uuid.UUID(str(self.pk)).bytes).decode("utf-8")

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email


class Client(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("User"),
        help_text=_("The user associated with this client."),
    )
    city = models.CharField(
        max_length=255,
        verbose_name=_("City"),
        help_text=_("The city where the client lives."),
        null=True,
        blank=True,
    )
    date_of_birth = models.DateField(
        verbose_name=_("Date of Birth"),
        help_text=_("The client's date of birth."),
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        verbose_name=_("Gender"),
        help_text=_("The client's gender."),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.city or ''})".strip()
