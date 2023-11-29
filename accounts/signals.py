from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import User

superuser = settings.SUPERUSER


@receiver(post_migrate)
def create_users(sender, **kwargs):
    if User.objects.filter(username=superuser["username"]).exists():
        return

    User.objects.create_superuser(
        superuser["username"], superuser["email"], superuser["password"]
    )
