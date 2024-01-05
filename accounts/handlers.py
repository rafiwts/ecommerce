import random
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def image_directory_path(instance, filename):
    now = datetime.now()
    full_name = f"{instance.first_name} {instance.last_name}"
    return f"{instance.id}-{full_name}-{now}-{filename}"


def generate_client_id_handler():
    while True:
        client_id = random.randint(1000000, 9999999)
        if not get_user_model().objects.filter(account__client_id=client_id).exists():
            return client_id


def reset_password_email_handler(request, user, email):
    company_email = settings.EMAIL_HOST_USER
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    reset_url = request.build_absolute_uri(
        reverse(
            "account:reset-password-confirmation",
            kwargs={"uidb64": uid, "token": token},
        )
    )
    subject = "Password Reset"
    message = render_to_string(
        "account/reset-password-email.html",
        {"reset_url": reset_url, "user": user},
    )

    try:
        send_mail(subject, message, company_email, [email])
        messages.success(request, "Password reset email sent. Check your inbox.")
    except Exception:
        messages.success(
            request, "Internal error. The message has not been sent. Try again."
        )


def upload_image_handler(request, user):
    if user.account.image:
        messages.info(request, "The profile image has been changed!")
    else:
        messages.info(request, "The new profile image has been added!")
