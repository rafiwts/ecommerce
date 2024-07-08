from django.urls import path

from .views import crete_coupon

app_name = "coupon"

urlpatterns = [
    path("add-coupon", crete_coupon, name="add-coupon"),
]
