from django.contrib import admin

from .models import Category, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_id",
        "name",
        "slug",
        "category",
        "user",
        "image",
        "price",
        "in_stock",
        "stock",
    ]
    list_filter = ["user", "category", "price", "in_stock"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "name",
                    "slug",
                    "category",
                    "price",
                    "in_stock",
                    "stock",
                    "image",
                    "description",
                ]
            },
        )
    ]
    search_fields = ["user", "name", "product_id"]
    ordering = ["id", "product_id", "price", "in_stock", "stock"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]
    list_filter = ["id", "name"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                ]
            },
        )
    ]
    search_fields = ["name"]
    ordering = ["id", "name"]
    prepopulated_fields = {"slug": ("name",)}
