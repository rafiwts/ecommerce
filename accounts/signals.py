from django.conf import settings
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import Account, AccountType, User

superuser = settings.SUPERUSER


@receiver(post_migrate)
def create_superuser_and_account_types(sender, **kwargs):
    if not AccountType.objects.exists():
        account_types = [
            AccountType(name="Basic"),
            AccountType(name="Premium", discount_value=5),
            AccountType(name="Golden", discount_value=10),
        ]

        AccountType.objects.bulk_create(account_types)

    if User.objects.filter(username=superuser["username"]).exists():
        return

    User.objects.create_superuser(
        superuser["username"], superuser["email"], superuser["password"]
    )


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
