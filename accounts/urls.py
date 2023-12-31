from django.urls import path

from .views import (
    change_password,
    create_profile,
    edit_account,
    edit_address,
    login_view,
    logout_view,
    profile_view,
    register,
    reset_password,
    reset_password_confirmation,
)

app_name = "account"

urlpatterns = [
    path("register/", register, name="register"),
    path(
        "reset-password/<uidb64>/<token>/",
        reset_password_confirmation,
        name="reset-password-confirmation",
    ),
    path("reset-password/", reset_password, name="reset-password"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("create-profile/", create_profile, name="create-profile"),
    path("<username>/", profile_view, name="profile-view"),
    path("<username>/edit-account/", edit_account, name="edit-account"),
    path("<username>/edit-address/", edit_address, name="edit-address"),
    path("<username>/change-password/", change_password, name="change-password"),
]
