from django.urls import path

from .views import (
    ChangePassword,
    ChangeProfileImage,
    EditAccount,
    EditAddress,
    ProfileView,
    ShippingAddressCreateView,
    ShippingAddressDeleteView,
    ShippingAddressUpdateView,
    create_profile,
    login_view,
    logout_view,
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
    path(
        "change-profile-image/",
        ChangeProfileImage.as_view(),
        name="change-profile-image",
    ),
    path("<str:username>/", ProfileView.as_view(), name="profile-view"),
    path("<str:username>/edit-account/", EditAccount.as_view(), name="edit-account"),
    path("<str:username>/edit-address/", EditAddress.as_view(), name="edit-address"),
    path(
        "<str:username>/change-password/",
        ChangePassword.as_view(),
        name="change-password",
    ),
    path(
        "shipping-address/<str:username>/add/",
        ShippingAddressCreateView.as_view(),
        name="shipping-address-add",
    ),
    path(
        "<str:username>/<int:address_id>/edit/",
        ShippingAddressUpdateView.as_view(),
        name="update-shipping-address",
    ),
    path(
        "<str:username>/<int:address_id>/delete/",
        ShippingAddressDeleteView.as_view(),
        name="delete-shipping-address",
    ),
]
