from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import User


class Coupon(models.Model):
    # add checking if the coupon is valid or not - the
    # coupon can be added manually or automatically
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coupons")
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(editable=False, null=True, blank=True)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField()

    @property
    def is_valid(self):
        current_time = timezone.now()
        is_active = self.valid_from <= current_time <= self.valid_to

        if self.active != is_active:
            self.active = is_active

        return is_active

    def save(self, *args, **kwargs):
        if not self.valid_from:
            self.valid_from = timezone.now()

        self.valid_to = self.valid_from + timedelta(weeks=2)
        self.active = self.is_valid

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.code

    class Meta:
        db_table = "coupons"
        ordering = ["code"]
        verbose_name = "coupon"
        indexes = [
            models.Index(fields=["id", "code"]),
        ]
