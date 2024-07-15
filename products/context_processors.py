from cart.cart import Cart

from .models import Category, Product


def categories_processor(request):
    categories = Category.objects.all()

    if request.user:
        favorite_count = Product.objects.filter(
            favoriteproduct__user=request.user
        ).count()

    cart = Cart(request)
    cart_length = len(cart)

    context = {
        "categories": categories,
        "favorite_count": favorite_count,
        "cart_length": cart_length,
    }

    return context
