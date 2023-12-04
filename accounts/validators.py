import re

from django.core.exceptions import ValidationError

from accounts.models import User


def password_validation(password):
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password has no uppercase letter")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password has no digit")


def email_validation(email):
    if User.objects.filter(email=email):
        raise ValidationError(f"The email {email} already exists")
