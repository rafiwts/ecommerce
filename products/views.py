import json

from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.list import ListView
from haystack.exceptions import SearchBackendError
from haystack.query import SearchQuerySet

from cart.forms import ProductCartAddForm

from .forms import ProductForm, ProductImageForm
from .models import Category, FavoriteProduct, Product, ProductImage
from .utils import get_recommendations, handle_last_seen_products


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


class BaseProductListView(ListView):
    model = Product
    # TODO: change pagination
    paginate_by = 5
    template_name = "product/home-page-product-list.html"
    context_object_name = "products"

    def get_queryset(self):
        return (
            self.model.objects.all()
        )  # Default queryset, should be overridden in subclasses

    def get_context_data(self, **kwargs):
        # add context to all child views
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["favorite_product_ids"] = FavoriteProduct.objects.filter(
                user=self.request.user
            ).values_list("product_id", flat=True)
        else:
            context["favorite_product_ids"] = []

        # add a form for displaying cart
        context["cart_product_form"] = ProductCartAddForm()

        return context

    def get_template_names(self):
        if self.template_name:
            return [self.template_name]
        return super().get_template_names()


class ProductListHomePageView(BaseProductListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # random sponsored products
        sponsored_products = Product.objects.filter(sponsored=True).order_by("?")[:10]

        # random products from random category
        random_category = Category.objects.order_by("?").first()
        category_products = (
            self.get_products_by_category(random_category) if random_category else []
        )

        # random for sale products
        sale_products = Product.objects.filter(for_sale__gt=0).order_by("?")[:10]

        # random for favorite products
        favorite_products = self.get_favorite_products(self.request.user)

        # handle last seen products
        last_seen_products_ids = handle_last_seen_products(self.request)
        last_seen_products = Product.objects.filter(id__in=last_seen_products_ids)

        # handle recommended products
        recommendations = get_recommendations(last_seen_products, favorite_products)

        # TODO: later add last bought

        context.update(
            {
                "sponsored_products": sponsored_products,
                "random_category": random_category,
                "category_products": category_products,
                "sale_products": sale_products,
                "favorite_products": favorite_products,
                "last_seen_products": last_seen_products,
                "recommended_products": recommendations,
            }
        )

        return context

    def get_favorite_products(self, user):
        if user.is_authenticated:
            return Product.objects.filter(
                id__in=user.favorite_products.values_list("product_id", flat=True)
            )
        return Product.objects.none()

    def get_products_by_category(self, category):
        return Product.objects.filter(
            child_subcategory__subcategory__category=category
        ).order_by("?")[:10]


class ProductListCategoryView(SingleObjectMixin, BaseProductListView):
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


class CustomProductListView(BaseProductListView):
    template_name = "product/custom-product-list.html"
    supported_query_types = ["sponsored", "sale", "favorite"]

    def get(self, request, *args, **kwargs):
        self.query_type = self.kwargs.get("type", None)
        if self.query_type and self.query_type not in self.supported_query_types:
            self.query_type = None
            return self.handle_invalid_query_type(request)

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        try:
            if self.query_type == "sponsored":
                return Product.objects.filter(sponsored=True)
            elif self.query_type == "sale":
                return Product.objects.filter(for_sale__gt=0)
            elif self.query_type == "favorite":
                return Product.objects.filter(favoriteproduct__user=self.request.user)
        except Exception as e:
            print(f"Error occured while fetching a queryset: {e}")
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type = self.query_type
        context["type"] = type

        return context

    def handle_invalid_query_type(self, request):
        raise Http404("Invalid query type")


class ProductListSearchView(BaseProductListView):
    template_name = "product/product-search.html"
    context_object_name = "results"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()

        if query:
            try:
                return SearchQuerySet().filter(name__startswith=query)
            except SearchBackendError as e:
                print(f"Search backend error: {e}")
            except Exception as e:
                print(f"An unexpected error occured: {e}")
        return SearchQuerySet().none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["query"] = query
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "product/product-detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["favorite_product_ids"] = FavoriteProduct.objects.filter(
                user=self.request.user
            ).values_list("product_id", flat=True)
        else:
            context["favorite_product_ids"] = []

        # add a form for displaying cart
        context["cart_product_form"] = ProductCartAddForm()

        # handle last seen products
        self.last_seen_products = handle_last_seen_products(
            self.request, self.object.id
        )
        last_seen_products = Product.objects.filter(id__in=self.last_seen_products)
        context["last_seen_products"] = last_seen_products

        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        response.set_cookie("last_seen_products", json.dumps(self.last_seen_products))
        return response


@login_required
def toggle_favorite(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        favorite, created = FavoriteProduct.objects.get_or_create(
            user=request.user, product=product
        )

        if not created:
            favorite.delete()
            return JsonResponse({"status": "removed"})
        return JsonResponse({"status": "added"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def autocomplete(request):
    # TODO: add recently seen at the very beginning and sponsored
    query = request.GET.get("q", "")
    suggestions = []

    if query:
        categories = Category.objects.filter(name__icontains=query)
        category_suggestions = [
            {
                "type": "category",
                "name": category.name,
                "id": category.id,
                "url": reverse("product:category-products", args=[category.slug]),
            }
            for category in categories
        ]

        products = Product.objects.filter(name__icontains=query)[:10]
        product_suggestions = [
            {
                "type": "product",
                "name": product.name,
                "id": product.id,
                "url": product.get_absolute_url(),
                "child_subcategory": product.child_subcategory.name,
                "subcategory": product.child_subcategory.subcategory.name,
                "category": product.child_subcategory.subcategory.category.name,
            }
            for product in products
        ]

        suggestions = category_suggestions + product_suggestions

    return JsonResponse(suggestions, safe=False)


# TODO: shop - all products and apply filters
# TODO: add vendors/companies
# TODO: add coupons to a cart
# TODO: for sale - 4 categories with for sale - random
# TODO: add tabs
# TODO: add some tabs to site and add active to it - fix activation
