import os
import uuid

from django.db import models
from django.utils.text import slugify

from accounts.models import User
from products.handlers import generate_product_id_handler, image_directory_path


class SligifiedModelMixin(models.Model):
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # if the slug already exists
            ModelClass = self.__class__
            while ModelClass.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Product(SligifiedModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    child_subcategory = models.ForeignKey(
        "ChildSubcategory", on_delete=models.CASCADE, related_name="products"
    )
    product_id = models.IntegerField(unique=True, verbose_name="Product ID")
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to=image_directory_path,
        null=True,
        blank=True,
        verbose_name="product picture",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255)
    stock = models.PositiveBigIntegerField()
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="When the product was added",
        verbose_name="added",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="When the product was updated",
        verbose_name="updated",
    )

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_id = generate_product_id_handler()
            while Product.objects.filter(product_id=self.product_id).exists():
                self.product_id = generate_product_id_handler()

        if self.pk:
            try:
                old_instance = Product.objects.get(pk=self.pk)
                # when image field has been updated
                if old_instance.image and old_instance.image != self.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except Product.DoesNotExist:
                pass

        super().save(*args, *kwargs)

    def delete(self, *args, **kwargs):
        """
        deleting image from media directory when user removed from database
        """
        if self.image:
            image = self.image
            if os.path.isfile(image.path):
                os.remove(image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "products"
        ordering = ["-created_at", "name"]
        verbose_name = "product"
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["child_subcategory"]),
        ]


class ChildSubcategory(SligifiedModelMixin):
    name = models.CharField(max_length=255, unique=True)
    subcategory = models.ForeignKey(
        "Subcategory", on_delete=models.CASCADE, related_name="chisubcategories"
    )
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "childsubcategories"
        ordering = ["-created_at", "name"]
        verbose_name = "childsubcategory"
        verbose_name_plural = "childsubcategories"
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["name"])]


class Subcategory(SligifiedModelMixin):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="subcategories"
    )
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "subcategories"
        ordering = ["-created_at", "name"]
        verbose_name = "subcategory"
        verbose_name_plural = "subcategories"
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["name"])]


class Category(SligifiedModelMixin):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="When the category was added",
        verbose_name="added",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        help_text="When the category was updated",
        verbose_name="updated",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        ordering = ["-created_at", "name"]
        verbose_name = "category"
        verbose_name_plural = "categories"
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["name"])]
