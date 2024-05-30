from django import forms
from django.core.validators import MaxLengthValidator

from .models import ChildSubcategory, Product


class ProductForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        required=False,
        widget=forms.FileInput(
            attrs={"id": "addProductImage", "class": "add-product-image"}
        ),
    )
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
    child_subcategory = forms.ModelChoiceField(
        queryset=ChildSubcategory.objects.all(),
        widget=forms.Select(attrs={"class": "product-subcategory"}),
        empty_label="Select a subcategory",
        label="Subcategory",
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

    class Meta:
        model = Product
        fields = ["image", "name", "description", "child_subcategory", "stock", "price"]

    def save(self, commit=True, user=None):
        # automatically add a user
        product = super().save(commit=False)
        if user:
            product.user = user
        if commit:
            product.save()
        return product
