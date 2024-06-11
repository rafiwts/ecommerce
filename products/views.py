from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ProductForm, ProductImageForm
from .models import ProductImage


def add_product_images(request):
    image_formset = modelformset_factory(ProductImage, form=ProductImageForm, extra=10)
    uploaded_images = []
    if request.method == "POST":
        formset = image_formset(
            data=request.POST, files=request.FILES, queryset=ProductImage.objects.none()
        )
        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:
                    image = form["image"]
                    uploaded_images.append(image)

        return add_product_info(request, *uploaded_images)
    else:
        formset = image_formset(queryset=ProductImage.objects.none())

    return render(request, "product/add-product-images.html", {"formset": formset})


def add_product_info(request, *args):
    # FIXME: fix the issue with passing a parameter
    uploaded_images = args
    print(uploaded_images)
    print(request.method)
    if request.method == "POST":
        product_form = ProductForm(data=request.POST)
        if product_form.is_valid():
            # workaround for deleting cat and subcat from cleaned data
            cleaned_data = product_form.cleaned_data
            category = cleaned_data.pop("category", None)
            subcategory = cleaned_data.pop("subcategory", None)

            product = product_form.save(commit=False, user=request.user)
            product.category = category
            product.subcategory = subcategory
            product.save(user=request.user)

            for form in uploaded_images:
                if form:
                    image = form["image"]
                    photo = ProductImage(product=product, image=image)
                    photo.save()

            return redirect(reverse("home"))

    else:
        product_form = ProductForm()

    context = {
        "product_form": product_form,
    }

    # if there is field error, retain the chosen categories
    if request.method == "POST":
        context.update(
            {
                "selected_category": request.POST.get("category"),
                "selected_subcategory": request.POST.get("subcategory"),
                "selected_child_subcategory": request.POST.get("child_subcategory"),
            }
        )

    return render(request, "product/add-product-info.html", context)


# TODO: chosen files disappear when form is invalid - perhaps js will solve the issue?
# TODO: verify the labels
# TODO: price cannot be negative
# TODO: see allegro what can be also added
# TODO: add it somewhere and only when the user is logged in and work on the display
