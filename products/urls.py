from django.urls import path

from .views import add_product

app_name = "product"

urlpatterns = [path("add-product/", add_product, name="add-product")]
