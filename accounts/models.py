import os

from django.contrib.auth.models import AbstractUser
from django.db import models

from .handlers import image_directory_path


# TODO: apply login to a website
class User(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"


# TODO: think what you can add to account type
class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discount_value = models.PositiveIntegerField(
        default=0, help_text="Discount value for a user", verbose_name="discount"
    )
    # TODO: add duration and function that checks if you still have valid account type

    def __str__(self):
        return self.name

    class Meta:
        db_table = "account_types"


class Account(models.Model):
    address = models.OneToOneField(
        "UserAddress", on_delete=models.SET_NULL, null=True, blank=True
    )
    account_type = models.ForeignKey(
        AccountType, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.OneToOneField(
        "User", on_delete=models.SET_NULL, null=True, blank=True, related_name="account"
    )
    first_name = models.CharField(max_length=100, null=False, verbose_name="name")
    last_name = models.CharField(max_length=100, null=False, verbose_name="surname")
    image = models.ImageField(
        upload_to=image_directory_path,
        null=True,
        blank=True,
        verbose_name="profile picture",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="When the account was created",
        verbose_name="created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="When the account was updated",
        verbose_name="updated",
    )

    def save(self, *args, **kwargs):
        """
        deleting image from media directory when image removed from database
        """
        if self.pk:
            try:
                old_instance = Account.objects.get(pk=self.pk)
                # when image field has been updated
                if old_instance.image and old_instance.image != self.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except Account.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ "
        deleting image from media directory when user removed from database
        """
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "accounts"
        ordering = ["-created_at", "last_name"]


class UserAddress(models.Model):
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=15, verbose_name="zip code")
    city = models.CharField(max_length=50)
    state = models.CharField(
        max_length=50, help_text="The name of the province in which you live"
    )
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"

    class Meta:
        db_table = "addresses"
        verbose_name_plural = "User addresses"
