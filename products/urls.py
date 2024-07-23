from django.urls import path

from .views import (
    CustomProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductListCategoryView,
    ProductListHomePageView,
    ProductListSearchView,
    autocomplete,
    toggle_favorite,
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
    path("favorite/toggle/<int:product_id>/", toggle_favorite, name="toggle-favorite"),
    path(
        "products/<str:type>/",
        CustomProductListView.as_view(),
        name="custom-product-list",
    ),
    path("search/", ProductListSearchView.as_view(), name="product-search"),
    path("autocomplete/", autocomplete, name="autocomplete"),
    path("<pk>/", ProductDetailView.as_view(), name="product-detail"),
]
