from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import ProductForm, ProductImageForm
from .models import Product, ProductImage


class ProductCreateView(View):
    login_required = True
    template_name_images = "product/add-product-images.html"
    template_name_info = "product/add-product-info.html"

    def get(self, request, step="info"):
        if step == "info":
            product_form = ProductForm()
            return render(
                request, self.template_name_info, {"product_form": product_form}
            )
        else:
            formset = self.get_image_formset()
            return render(request, self.template_name_images, {"formset": formset})

    def post(self, request, step="info"):
        if step == "images":
            formset = self.get_image_formset(data=request.POST, files=request.FILES)
            if formset.is_valid():
                product = self.get_product_from_session(request)
                for form in formset.cleaned_data:
                    if form:
                        image = form["image"]
                        product_image = ProductImage(product=product, image=image)
                        product_image.save()

                self.clear_product_from_session(request)

                return redirect(reverse("home"))

            return render(request, self.template_name_images, {"formset": formset})
        elif step == "info":
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

                self.save_product_to_session(request, product)

                return redirect(
                    reverse("product:add-product", kwargs={"step": "images"})
                )

            context = {
                "product_form": product_form,
            }

            # if there is field error, retain the chosen categories
            if request.method == "POST":
                context.update(
                    {
                        "selected_category": request.POST.get("category"),
                        "selected_subcategory": request.POST.get("subcategory"),
                        "selected_child_subcategory": request.POST.get(
                            "child_subcategory"
                        ),
                    }
                )

            return render(request, "product/add-product-info.html", context)

    def get_image_formset(self, data=None, files=None):
        ImageFormSet = modelformset_factory(
            ProductImage, form=ProductImageForm, extra=10
        )
        if data:
            return ImageFormSet(
                data=data, files=files, queryset=ProductImage.objects.none()
            )
        return ImageFormSet(queryset=ProductImage.objects.none())

    def get_product_from_session(self, request):
        product_id = request.session.get("product_id")
        if product_id:
            try:
                return Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return None
        return None

    def save_product_to_session(self, request, product):
        request.session["product_id"] = product.id

    def clear_product_from_session(self, request):
        if "product_id" in request.session:
            del request.session["product_id"]


# TODO: sponsored - first look view in
#  home/then recommended/ last seen /favourite /four random categories
# TODO: add
# categories to a drop down list - a random query
# of a list of products from a given category
# TODO: add for sale and sponsored to model - sale as a choice of percentage
# TODO: add vendors/companies
# TODO: shop - all products and apply filters
# TODO: for sale - 4 categories with for sale - random
# TODO: search bar - make a use of it
