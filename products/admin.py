from django.contrib import admin

from .models import Category, ChildSubcategory, Product, Subcategory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_id",
        "name",
        "slug",
        "child_subcategory",
        "user",
        "image",
        "price",
        "in_stock",
        "stock",
    ]
    list_filter = ["user", "child_subcategory", "price", "in_stock"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "user",
                    "name",
                    "slug",
                    "child_subcategory",
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


@admin.register(ChildSubcategory)
class ChildSubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "subcategory"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "subcategory",
                ]
            },
        )
    ]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "category"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "slug",
                    "category",
                ]
            },
        )
    ]
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
