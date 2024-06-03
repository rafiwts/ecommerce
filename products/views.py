from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProductForm, ProductImageForm
from .models import ProductImage


def add_product(request):
    ImageFormSet = modelformset_factory(
        ProductImage, form=ProductImageForm, extra=3, can_delete=True
    )
    if request.method == "POST":
        product_form = ProductForm(data=request.POST)
        formset = ImageFormSet(
            data=request.POST, files=request.FILES, queryset=ProductImage.objects.none()
        )
        if product_form.is_valid() and formset.is_valid():
            # workaround for deleting cat and subcat from cleaned data
            cleaned_data = product_form.cleaned_data
            category = cleaned_data.pop("category", None)
            subcategory = cleaned_data.pop("subcategory", None)

            product = product_form.save(commit=False, user=request.user)
            product.category = category
            product.subcategory = subcategory
            product.save(user=request.user)

            for form in formset.cleaned_data:
                if form:
                    image = form["image"]
                    photo = ProductImage(product=product, image=image)
                    photo.save()

            return redirect(reverse("home"))
    else:
        product_form = ProductForm()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    return render(
        request,
        "product/add-product.html",
        {"product_form": product_form, "formset": formset},
    )


# TODO: think how to add many images to one product - not only one
# improve how to add it - one more if all pictures added
# check JS and view
# and also the main image and it moves and dispalys
# TODO: stock and price cannot be negative
# TODO: see allegro what can be also added
# TODO: add it somewhere and only when the user is logged in and work on the display
# TODO:
# TODO:
# TODO:
# TODO:
