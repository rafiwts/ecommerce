from django.urls import path

from .views import (
    change_password,
    create_profile,
    edit_profile,
    login_view,
    logout_view,
    profile_view,
    register,
)

app_name = "account"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("create-profile/", create_profile, name="create-profile"),
    path("<username>/", profile_view, name="profile-view"),
    path("<username>/edit-profile/", edit_profile, name="edit-profile"),
    path("<username>/change-password", change_password, name="change-password"),
]
