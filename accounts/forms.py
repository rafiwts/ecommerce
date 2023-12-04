from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Account, User

from .validators import email_validation, password_validation


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SingUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text="Choose unique username")
    email = forms.EmailField(
        max_length=100,
        help_text="Enter a valid email address",
        validators=[email_validation],
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        validators=[password_validation],
        help_text=(
            "Password must contain at least 8 characters "
            "with one uppercase and one digit"
        ),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Confirm the password",
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return password2


class EditAccountForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label="First name", required=True)
    last_name = forms.CharField(max_length=50, label="Surname", required=True)
    date_of_birth = forms.DateField(
        label="Birth date",
        widget=forms.DateInput(attrs={"type": "date"}),
        required=True,
        input_formats=["%Y-%m-%d"],
    )

    class Meta:
        model = Account
        fields = ["first_name", "last_name", "date_of_birth", "image"]
