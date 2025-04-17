from typing import Any
from django.utils.translation import gettext_lazy as _

from django.db import models


class GenderChoices(models.TextChoices):
    MALE: Any = "MALE", _("Male")
    FEMALE: Any = "FEMALE", _("Female")
