import os
import uuid
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from products.handlers import generate_product_id_handler, image_directory_path


class ProductModelMixin(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    class Meta:
        abstract = True


class Product(ProductModelMixin):
    DISCOUNT_CHOICES = [
        (0, "0%"),
        (5, "5%"),
        (10, "10%"),
        (15, "15%"),
        (20, "20%"),
        (25, "25%"),
        (30, "30%"),
        (35, "35%"),
        (40, "40%"),
        (45, "45%"),
        (50, "50%"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    child_subcategory = models.ForeignKey(
        "ChildSubcategory", on_delete=models.CASCADE, related_name="products"
    )
    product_id = models.IntegerField(unique=True, verbose_name="Product ID")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reduced_price = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=255)
    stock = models.PositiveBigIntegerField()
    in_stock = models.BooleanField(default=True)
    for_sale = models.PositiveBigIntegerField(choices=DISCOUNT_CHOICES, default=0)
    # TODO: think about types of it
    sponsored = models.BooleanField(default=False)
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
        if not self.slug:
            self.slug = slugify(self.name)
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"

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

        if self.for_sale:
            discount = self.for_sale / Decimal(100)
            discounted_price = self.price * (Decimal(1) - discount)
            self.reduced_price = discounted_price

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

    def get_absolute_url(self):
        return reverse("product:product-detail", args=[str(self.id)])

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


class ChildSubcategory(ProductModelMixin):
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


class Subcategory(ProductModelMixin):
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


class Category(ProductModelMixin):
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


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=image_directory_path,
        null=True,
        blank=True,
        verbose_name="product picture",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_instance = ProductImage.objects.get(pk=self.pk)
                # when image field has been updated
                if old_instance.image and old_instance.image != self.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except ProductImage.DoesNotExist:
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
        return self.image

    class Meta:
        db_table = "product_images"
        ordering = ["-uploaded_at"]
        verbose_name = "product_image"
        indexes = [
            models.Index(fields=["id", "product"]),
        ]


class FavoriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    class Meta:
        unique_together = ("user", "product")
