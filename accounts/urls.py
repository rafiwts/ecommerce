from django.urls import path

from .views import account

app_name = "account"

urlpatterns = [
    path("account/", account, name="account"),
]
