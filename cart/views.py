from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product

from .cart import Cart
from .forms import ProductCartAddForm


@require_POST
def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = ProductCartAddForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.add(
            product=product, quantity=data["quantity"], update_quantity=data["update"]
        )

    return redirect("cart:cart_detail")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = ProductCartAddForm(
            initial={"quantity": item["quantity"], "update": True}
        )

    return render(request, "cart/cart-detail.html", {"cart": cart})
