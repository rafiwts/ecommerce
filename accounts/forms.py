from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Account, User, UserAddress

from .validators import email_validation, password_validation


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
                "autocomplete": "email",
            }
        ),
    )


class SingUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        label="Username",
        help_text="Choose unique username",
        widget=forms.TextInput(
            attrs={
                "class": "register-field",
                "id": "username",
                "autocomplete": "username",
            }
        ),
    )
    email = forms.EmailField(
        max_length=100,
        label="Email",
        help_text="Enter a valid email address",
        validators=[email_validation],
        widget=forms.EmailInput(
            attrs={"class": "register-field", "id": "email", "autocomplete": "email"}
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
                "id": "password1",
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
                "id": "password2",
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


class AccountForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        label="First name",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "account-password-field",
                "id": "first_name",
                "autocomplete": "on",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        label="Surname",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "account-password-field",
                "id": "last_name",
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
                "class": "account-password-field",
                "id": "date_of_birth",
                "autocomplete": "off",
            }
        ),
    )
    image = forms.ImageField(
        label="Image", required=False, widget=forms.FileInput(attrs={"id": "image"})
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "date_of_birth", "image"]


class UserAddressForm(forms.ModelForm):
    street = forms.CharField(
        max_length=50,
        label="Street",
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "street", "autocomplete": "on"}
        ),
    )
    zip_code = forms.CharField(
        max_length=50,
        label="Zip code",
        widget=forms.TextInput(
            attrs={
                "class": "edit-address-field",
                "id": "zip_code",
                "autocomplete": "on",
            }
        ),
    )
    city = forms.CharField(
        max_length=100,
        label="City",
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "city", "autocomplete": "on"}
        ),
    )
    state = forms.CharField(
        max_length=50,
        label="Stage",
        help_text="The name of the province in which you live",
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "state", "autocomplete": "on"}
        ),
    )
    country = forms.CharField(
        max_length=50,
        label="Country",
        widget=forms.TextInput(
            attrs={"class": "edit-address-field", "id": "country", "autocomplete": "on"}
        ),
    )

    class Meta:
        model = UserAddress
        fields = ["street", "zip_code", "city", "state", "country"]


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(
        label="Old password",
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "change-password-field",
                "id": "old_password",
                "autocomplete": "off",
            }
        ),
    )
    new_password = forms.CharField(
        label="New password",
        validators=[password_validation],
        widget=forms.PasswordInput(
            attrs={
                "class": "change-password-field",
                "id": "new_password",
                "autocomplete": "off",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="Confirm password",
        help_text=(
            "Password must contain at least 8 characters "
            "with one uppercase and one digit"
        ),
        widget=forms.PasswordInput(
            attrs={
                "class": "change-password-field",
                "id": "confirm_password",
                "autocomplete": "off",
            }
        ),
    )
