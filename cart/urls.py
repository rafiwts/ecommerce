from django.urls import path

from .views import add_to_cart, cart_detail, remove_from_cart

app_name = "cart"

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path("add/<int:product_id>/", add_to_cart, name="cart_add"),
    path("remove/<int:product_id>/", remove_from_cart, name="cart_remove"),
]
