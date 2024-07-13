from django.contrib import admin

from .models import (
    Category,
    ChildSubcategory,
    FavoriteProduct,
    Product,
    ProductImage,
    Subcategory,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "product_id",
        "name",
        "slug",
        "child_subcategory",
        "user",
        "formatted_price",
        "in_stock",
        "stock",
    ]
    list_filter = [
        "user",
        "child_subcategory__subcategory__category",
        "price",
        "in_stock",
    ]
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
                    "description",
                ]
            },
        )
    ]
    search_fields = ["user__username", "name", "product_id"]
    ordering = ["id", "product_id", "in_stock", "stock"]
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ["user", "child_subcategory"]

    def formatted_price(self, obj):
        return f"$ {obj.price:.2f}"

    formatted_price.short_description = "Price"


@admin.register(ChildSubcategory)
class ChildSubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "subcategory", "slug"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "subcategory",
                    "slug",
                ]
            },
        )
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ["subcategory"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "slug"]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "category",
                    "slug",
                ]
            },
        )
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_select_related = ["category"]


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


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["product", "image"]
    list_filter = ["product__user"]
    search_fields = ["product"]
    ordering = ["product"]


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ["product", "user"]
