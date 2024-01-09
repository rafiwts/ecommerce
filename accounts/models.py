import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .handlers import image_directory_path


class User(AbstractUser):
    def delete(self, *args, **kwargs):
        """
        deleting image from media directory when user removed from database
        """
        try:
            account = Account.objects.get(user=self.id)
            if account.image:
                image = account.image
                if os.path.isfile(image.path):
                    os.remove(image.path)
        except Account.DoesNotExist:
            pass

        return super().delete(*args, **kwargs)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"


class Account(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, null=True, blank=True, related_name="account"
    )
    account = models.OneToOneField(
        "AccountType", on_delete=models.SET_NULL, null=True, blank=True
    )
    client_id = models.IntegerField(null=True, blank=True, verbose_name="Client ID")
    first_name = models.CharField(max_length=100, null=False, verbose_name="name")
    last_name = models.CharField(max_length=100, null=False, verbose_name="surname")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Birth date")
    image = models.ImageField(
        upload_to=image_directory_path,
        null=True,
        blank=True,
        verbose_name="profile picture",
    )
    phone = PhoneNumberField(null=True, blank=True, unique=True)
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

    @property
    def account_type_default(self):
        return self.account or "No premium account"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def delete(self, *args, **kwargs):
        """
        deleting image from media directory when user removed from database
        """
        if self.image:
            image = self.image
            if os.path.isfile(image.path):
                os.remove(image.path)

        super().delete(*args, **kwargs)

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "accounts"
        ordering = ["-created_at", "last_name"]


# TODO: think what you can add to account type
class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    discount_value = models.PositiveIntegerField(
        default=0, help_text="Discount value for a user", verbose_name="discount"
    )
    # TODO: add duration and function that checks if you still have valid account type

    def __str__(self):
        return self.name


class Adress(models.Model):
    street = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=15, verbose_name="zip code")
    city = models.CharField(max_length=50)
    state = models.CharField(
        max_length=50,
        help_text="The name of the province in which you live",
    )
    country = models.CharField(max_length=50)

    def get_full_address(self):
        if self.city:
            return (
                f"{self.street}, {self.zip_code}\n" f"{self.city}\n" f"{self.country}"
            )
        else:
            return False

    def __str__(self):
        address_components = [self.street, self.zip_code, self.city, self.country]
        if address_components:
            non_empty_components = [
                component for component in address_components if component
            ]
            return ", ".join(non_empty_components)

        return None

    class Meta:
        abstract = True


class UserShippingAddress(Adress):
    account = models.ForeignKey(
        "Account",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shipping_addresses",
    )

    class Meta:
        db_table = "shipping_addresses"
        verbose_name_plural = "User shipping addresses"


class UserAddress(Adress):
    account = models.OneToOneField(
        "Account",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="address",
    )

    class Meta:
        db_table = "addresses"
        verbose_name_plural = "User addresses"
