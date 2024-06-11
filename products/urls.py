from django.urls import path

from .views import add_product_images, add_product_info

app_name = "product"

urlpatterns = [
    path("add-product-images/", add_product_images, name="add-product-images"),
    path("add-product-info/", add_product_info, name="add-product-info"),
]
