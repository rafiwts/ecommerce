from django.urls import path

from .views import (
    CustomProductListView,
    ProductCreateView,
    ProductListCategoryView,
    ProductListHomePageView,
)

app_name = "product"

urlpatterns = [
    path("home-page/", ProductListHomePageView.as_view(), name="home-page-products"),
    path("add-product/<str:step>/", ProductCreateView.as_view(), name="add-product"),
    path("list-view/", ProductListCategoryView.as_view(), name="product-list"),
    path(
        "list-view/<slug:category_slug>/",
        ProductListCategoryView.as_view(),
        name="category-products",
    ),
    path("all-products/", ProductListCategoryView.as_view(), name="all-products"),
    path("<str:type>/", CustomProductListView.as_view(), name="custom-product-list"),
]
