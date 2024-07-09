from django.urls import path

from .views import ProductCreateView, ProductListView

app_name = "product"

urlpatterns = [
    path("add-product/<str:step>/", ProductCreateView.as_view(), name="add-product"),
    path("list-view", ProductListView.as_view(), name="product-list"),
    path(
        "list-view/<slug:category_slug>", ProductListView.as_view(), name="product-list"
    ),
]
