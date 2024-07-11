from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView

from .forms import ProductForm, ProductImageForm
from .models import Category, Product, ProductImage


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


class ProductListHomePageView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "product/home-page-product-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # random sponsored products
        sponsored_products = Product.objects.filter(sponsored=True).order_by("?")[:10]

        # random products from random category
        random_category = Category.objects.order_by("?").first()

        if random_category:
            category_products = Product.objects.filter(
                child_subcategory__subcategory__category=random_category
            ).order_by("?")[:10]

        # random for sale products
        for_sale_products = Product.objects.filter(for_sale__gt=0).order_by("?")[:10]

        # TODO: later add favorite, recommended, and recently seen

        context["sponsored_products"] = sponsored_products
        context["random_category"] = random_category
        context["category_products"] = category_products
        context["sale_products"] = for_sale_products

        return context


class ProductListCategoryView(SingleObjectMixin, ListView):
    model = Product
    paginate_by = 5
    template_name = "product/product-list.html"

    def get(self, request, *args, **kwargs):
        # Fetch the category object or return 404 if not found
        if "category_slug" in self.kwargs:
            self.object = get_object_or_404(Category, slug=self.kwargs["category_slug"])
        else:
            self.object = None
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_slug"] = self.kwargs.get("category_slug")
        context["category"] = self.object

        return context

    def get_queryset(self):
        if self.object:
            # if the category is chosen
            category = self.object
            return Product.objects.filter(
                child_subcategory__subcategory__category=category
            )
        return Product.objects.all()


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
