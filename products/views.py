from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProductForm


def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(data=request.POST, files=request.FILES)
        if product_form.is_valid():
            product_form.save(user=request.user)
            return redirect(reverse("home"))
    else:
        product_form = ProductForm()

    return render(request, "product/add-product.html", {"product_form": product_form})


# TODO: think how to add many images to one product - not only one
# and also the main image and it moves and dispalys
# TODO: think about how to choose a category>subcategory
# and then subchild and not only subchild
# TODO: stock and price cannot be negative
# TODO: see allegro what can be also added
# TODO: add it somewhere and only when the user is logged in and work on the display
# TODO:
# TODO:
# TODO:
# TODO:
