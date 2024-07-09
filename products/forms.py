from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from file_resubmit.admin import AdminResubmitFileWidget, AdminResubmitImageWidget

from .models import Category, ChildSubcategory, Product, ProductImage, Subcategory


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
        label="Name",
        required=True,
        widget=forms.TextInput(
            attrs={"id": "addProductName", "class": "add-product-name"}
        ),
    )
    description = forms.CharField(
        max_length=500,
        validators=[MaxLengthValidator(500)],
        label="Description",
        required=True,
        widget=forms.TextInput(
            attrs={"id": "addProductDescription", "class": "add-product-description"}
        ),
    )
    category = forms.ModelChoiceField(
        label="Category",
        required=True,
        queryset=Category.objects.all(),
    )
    subcategory = forms.ModelChoiceField(
        label="Subcategory",
        required=True,
        queryset=Subcategory.objects.all(),
    )
    child_subcategory = forms.ModelChoiceField(
        required=True,
        queryset=ChildSubcategory.objects.all(),
    )
    stock = forms.IntegerField(
        label="Stock",
        required=True,
        widget=forms.NumberInput(
            attrs={"id": "addProductStock", "class": "add-product-stock"}
        ),
    )
    price = forms.DecimalField(
        label="Price",
        required=True,
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(
            attrs={
                "id": "addProductPrice",
                "class": "add-product-price",
                "step": "0.01",
            }
        ),
    )
    for_sale = forms.ChoiceField(
        label="Discount",
        required=False,
        choices=Product.DISCOUNT_CHOICES,
        widget=forms.Select(
            attrs={"id": "addProductDiscount", "class": "add-product-discount"}
        ),
    )
    sponsored = forms.BooleanField(
        label="Sponsored",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"id": "addProductSponsored", "class": "add-product-sponsored"}
        ),
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "child_subcategory",
            "stock",
            "price",
            "for_sale",
            "sponsored",
        ]

    def save(self, commit=True, user=None):
        # automatically add a user
        product = super().save(commit=False)

        if user:
            product.user = user
        if commit:
            product.save()
        return product

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise ValidationError(
                "Please insert a correct price! It cannot be lower than 0!"
            )
        return price


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        widgets = {
            "picture": AdminResubmitImageWidget,
            "file": AdminResubmitFileWidget,
        }
        fields = ["image"]
