from django.urls import path

from .views import edit_profile, login_view, register

app_name = "account"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("edit-profile/", edit_profile, name="edit-profile"),
]
