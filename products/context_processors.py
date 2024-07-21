from django.core.exceptions import ObjectDoesNotExist

from cart.cart import Cart
from cart.utils import add_update_quantity_form_to_cart

from .models import Category, Product


def context_processor(request):
    try:
        categories = Category.objects.all()
    except ObjectDoesNotExist:
        categories = []

    if request.user.is_authenticated:
        try:
            favorite_count = Product.objects.filter(
                favoriteproduct__user=request.user
            ).count()
            favortie_products = Product.objects.filter(
                favoriteproduct__user=request.user
            )
        except ObjectDoesNotExist:
            favorite_count = 0
            favortie_products = []

    else:
        favorite_count = 0
        favortie_products = None

    cart = Cart(request)
    add_update_quantity_form_to_cart(cart)

    cart_length = len(cart)

    context = {
        "categories": categories,
        "favorite_count": favorite_count,
        "cart_length": cart_length,
        "favorite_products": favortie_products,
        "cart": cart,
    }

    return context
