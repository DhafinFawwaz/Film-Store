import functools
import gzip
import re
from difflib import SequenceMatcher
from pathlib import Path

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist,
    ImproperlyConfigured,
    ValidationError,
)
from django.utils.functional import cached_property, lazy
from django.utils.html import format_html, format_html_join
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.utils.translation import ngettext


class MinimumLengthValidator:
    """
    Validate that the password is of a minimum length.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    "Password at least "
                    "%(min_length)d character.",
                    "Password at least "
                    "%(min_length)d characters.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            "Password must contain at least %(min_length)d character.",
            "Password must contain at least %(min_length)d characters.",
            self.min_length,
        ) % {"min_length": self.min_length}


class HasDigitValidator:
    """
    Validate that the password has a digit.
    """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password: str, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                "Password must contain digit.",
                code="password_no_digit",
            )

    def get_help_text(self):
        return "Password must contain digit."
