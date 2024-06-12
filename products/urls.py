from django.urls import path

from .views import ProductCreateView

app_name = "product"

urlpatterns = [
    path("add-product/<str:step>/", ProductCreateView.as_view(), name="add-product"),
    path("add-product/<str:step>/", ProductCreateView.as_view(), name="add-product"),
]
