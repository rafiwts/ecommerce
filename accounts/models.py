from django.contrib.auth.models import AbstractUser
from django.db import models

from .handlers import image_directory_path


class User(AbstractUser):
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, null=True, blank=True, related_name="users"
    )

    def __str__(self):
        return self.username


# TODO: think what you can add to account type and apply models to admin site
class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discount_value = models.PositiveIntegerField(
        default=0, help_text="Discount value when 'discount' is True"
    )


# add verbose names and see admin fields
class Account(models.Model):
    address = models.ForeignKey(
        "UserAddress", on_delete=models.CASCADE, null=True, blank=True
    )
    account_type = models.ForeignKey(
        AccountType, on_delete=models.CASCADE, null=True, blank=True
    )
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to=image_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserAddress(models.Model):
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=15)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
