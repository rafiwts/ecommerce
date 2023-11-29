from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)


class User(AbstractUser):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.username
