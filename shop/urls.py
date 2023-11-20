from django.urls import path

from .views import contact, info, sale, shop, vendor

app_name = "shop"

urlpatterns = [
    path("shop/", shop, name="shop"),
    path("sale/", sale, name="sale"),
    path("vendor/", vendor, name="vendor"),
    path("info/", info, name="info"),
    path("contact/", contact, name="contact"),
]
