import re

from django.core.exceptions import ValidationError

from accounts.models import User


def password_validation(password):
    if not re.search(r"[A-Z]", password) and not re.search(r"\d", password):
        raise ValidationError(
            "New password must contain at least one uppercase letter and one digit."
        )
    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            "New password must contain at least one uppercase letter."
        )
    if not re.search(r"\d", password):
        raise ValidationError("New password must contain at least one digit.")


def email_validation(email):
    if User.objects.filter(email=email):
        raise ValidationError(f"The email {email} already exists")
