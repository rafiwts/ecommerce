import re

from django.core.exceptions import ValidationError


def password_validation(password):
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password has no uppercase letter")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password has no digit")
