from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from accounts.models import Account, User, UserAddress, UserShippingAddress

from .validators import email_validation, password_validation, username_validation


class NonstickyTextInput(forms.TextInput):
    # clear the submitted input box
    def get_context(self, name, value, attrs):
        value = None
        return super().get_context(name, value, attrs)


class NonstickyEmailInput(forms.EmailInput):
    def get_context(self, name, value, attrs):
        value = None
        return super().get_context(name, value, attrs)


class CustomTextInput(NonstickyTextInput, forms.TextInput):
    def __init__(self, attrs=None):
        NonstickyTextInput.__init__(self, attrs)
        forms.TextInput.__init__(self, attrs)


class CustomEmailInput(NonstickyEmailInput, forms.EmailInput):
    def __init__(self, attrs=None):
        NonstickyEmailInput.__init__(self, attrs)
        forms.EmailInput.__init__(self, attrs)


class SingUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        label="Username",
        help_text="Choose unique username",
        validators=[username_validation],
        widget=CustomTextInput(
            attrs={
                "class": "register-field",
                "id": "username",
                "autocomplete": "off",
            }
        ),
    )
    email = forms.EmailField(
        max_length=100,
        label="Email",
        help_text="Enter a valid email address",
        validators=[email_validation],
        widget=CustomEmailInput(
            attrs={"class": "register-field", "id": "email", "autocomplete": "off"}
        ),
    )
    password1 = forms.CharField(
        label="Password",
        help_text=(
            "Password must contain at least 8 characters "
            "with one uppercase and one digit"
        ),
        validators=[password_validation],
        widget=forms.PasswordInput(
            attrs={
                "class": "register-field",
                "id": "password",
                "autocomplete": "off",
            }
        ),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        help_text="Confirm the password",
        widget=forms.PasswordInput(
            attrs={
                "class": "register-field",
                "id": "password-confirm",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_password(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username or email",
        widget=forms.TextInput(
            attrs={
                "class": "login-field",
                "id": "username",
                "autocomplete": "off",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "login-field",
                "id": "password",
                "autocomplete": "off",
            }
        ),
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "reset-password-field",
                "id": "email",
                "autocomplete": "off",
                "placeholder": "email",
            }
        ),
    )


country_choices = [
    ("DE", "Germany"),
    ("FR", "France"),
    ("PL", "Poland"),
    ("RU", "Russia"),
    ("IT", "Italy"),
    ("ES", "Spain"),
    ("NO", "Norway"),
    ("UK", "The United Kingdom"),
]

sorted_country_choices = sorted(country_choices, key=lambda x: x[1])


class BaseAccountForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        label="First name",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "edit-account-field",
                "id": "firstName",
                "autocomplete": "on",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        label="Surname",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "edit-account-field",
                "id": "lastName",
                "autocomplete": "on",
            }
        ),
    )
    date_of_birth = forms.DateField(
        label="Birth date",
        required=True,
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "edit-account-field",
                "id": "dateOfBirth",
                "autocomplete": "off",
            }
        ),
    )
    phone = PhoneNumberField(
        label="Phone number",
        required=False,
        region="PL",
        widget=PhoneNumberPrefixWidget(
            initial="PL", country_choices=sorted_country_choices
        ),
    )

    class Meta:
        abstract = True


class EditAccoutForm(BaseAccountForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "date_of_birth", "phone"]


class CreateProfileForm(BaseAccountForm):
    # replace id for creating profile
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget = forms.TextInput(
            attrs={
                "class": "create-profile-field",
                "id": "firstNameProfile",
                "autocomplete": "on",
                "placeholder": "First name...",
            }
        )
        self.fields["last_name"].widget = forms.TextInput(
            attrs={
                "class": "create-profile-field",
                "id": "lastNameProfile",
                "autocomplete": "on",
                "placeholder": "Last name...",
            }
        )
        self.fields["date_of_birth"].widget = forms.DateInput(
            attrs={
                "type": "date",
                "class": "create-profile-field",
                "id": "birthDateProfile",
                "autocomplete": "off",
            }
        )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "date_of_birth", "phone"]


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label="Image",
        required=True,
        widget=forms.FileInput(
            attrs={
                "id": "uploadProfileImage",
                "class": "upload-profile-image",
            }
        ),
    )

    class Meta:
        model = Account
        fields = ("image",)


class BaseAddressForm(forms.ModelForm):
    street = forms.CharField(
        max_length=50,
        label="Street",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "street", "autocomplete": "on"}
        ),
    )
    zip_code = forms.CharField(
        max_length=50,
        label="Zip code",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "edit-address-field",
                "id": "zipCode",
                "autocomplete": "on",
            }
        ),
    )
    city = forms.CharField(
        max_length=50,
        label="City",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "city", "autocomplete": "on"}
        ),
    )
    state = forms.CharField(
        max_length=50,
        label="State",
        required=False,
        help_text="The name of the province in which you live",
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "state", "autocomplete": "on"}
        ),
    )
    country = forms.CharField(
        max_length=50,
        label="Country",
        required=False,
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "country", "autocomplete": "on"}
        ),
    )

    class Meta:
        abstract = True


class UserAddressForm(BaseAddressForm):
    class Meta(BaseAddressForm.Meta):
        model = UserAddress
        fields = ["street", "zip_code", "city", "state", "country"]


class UserShippingAddressForm(BaseAddressForm):
    company = forms.CharField(
        label="Company name", required=False, help_text="Company name is optional"
    )

    # replace id for shipping address
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["street"].widget = forms.TextInput(
            attrs={
                "class": "edit-address-field",
                "id": "streetAdd",
                "autocomplete": "on",
            }
        )
        self.fields["zip_code"].widget = forms.TextInput(
            attrs={
                "class": "edit-address-field",
                "id": "zipCodeAdd",
                "autocomplete": "on",
            }
        )
        self.fields["city"].widget = forms.TextInput(
            attrs={"class": "edit-address-field", "id": "cityAdd", "autocomplete": "on"}
        )
        self.fields["state"].widget = forms.TextInput(
            attrs={
                "class": "edit-address-field",
                "id": "stateAdd",
                "autocomplete": "on",
            }
        )
        self.fields["country"].widget = forms.TextInput(
            attrs={
                "class": "edit-address-field",
                "id": "countryAdd",
                "autocomplete": "on",
            }
        )

    class Meta(BaseAddressForm.Meta):
        model = UserShippingAddress
        fields = [
            "first_name",
            "last_name",
            "company",
            "street",
            "zip_code",
            "city",
            "state",
            "country",
        ]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Old password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "change-password-field",
                "id": "oldPassword",
                "autocomplete": "off",
                "placeholder": "Old password",
            }
        ),
    )
    new_password = forms.CharField(
        label="New password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "change-password-field",
                "id": "newPassword",
                "autocomplete": "off",
                "placeholder": "New password",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        required=False,
        help_text=(
            "Password must contain at least 8 characters "
            "with one uppercase and one digit"
        ),
        widget=forms.PasswordInput(
            attrs={
                "class": "change-password-field",
                "id": "confirmPassword",
                "autocomplete": "off",
                "placeholder": "Confirm password",
            }
        ),
    )
