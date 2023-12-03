from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User

from .validators import password_validation


class SingUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text="Choose unique username")
    email = forms.EmailField(max_length=100, help_text="Enter a valid email address")
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

    def check_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email="email"):
            raise forms.ValidationError(f"The email {email} already exists")
        return email

    def clean_password2(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2
