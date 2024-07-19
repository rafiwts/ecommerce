from django.shortcuts import render

from products.models import Category, Product


def home(request):
    categories = Category.objects.all()

    if request.user.is_authenticated:
        favortie_products = Product.objects.filter(favoriteproduct__user=request.user)
    else:
        favortie_products = None

    return render(
        request,
        "base.html",
        context={"categories": categories, "favorite_products": favortie_products},
    )
