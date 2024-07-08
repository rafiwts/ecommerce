from django import forms

from .models import Coupon


class CouponForm(forms.ModelForm):
    code = forms.CharField()
    discount = forms.IntegerField()
    valid_from = forms.DateField(
        label="Valid from",
        required=False,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "edit-account-field",
                "id": "validFrom",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = Coupon
        fields = ["code", "discount", "valid_from"]
