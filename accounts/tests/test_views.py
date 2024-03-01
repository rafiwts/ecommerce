import os

import pytest
from django.urls import reverse
from dotenv import load_dotenv

load_dotenv()


@pytest.mark.django_db
class TestView:
    @pytest.mark.parametrize(
        "template_name",
        {
            "home",
            "account:register",
            "account:login",
        },
    )
    def test_views_with_no_login_required(self, client, template_name):
        url = reverse(template_name)
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "template_name, login_user, password",
        {
            ("account:profile-view", "mako", "Stefan13!"),
            ("account:edit-account", "tako", "August13!"),
            ("account:edit-address", "bako", "Zygmunt13!"),
            (
                "account:change-password",
                "rafiwts",
                os.environ.get("SUPERUSER_PASSWORD"),
            ),
            ("account:shipping-address-add", "tako", "August13!"),
        },
    )
    def test_views_with_login_required(
        self, client, template_name, login_user, password, custom_users
    ):
        client.login(username=login_user, password=password)
        url = reverse(template_name, kwargs={"username": login_user})

        response = client.get(url)

        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    "login_user, password",
    [
        ("rafiwts", os.environ.get("SUPERUSER_PASSWORD")),
        ("rafiwts@ecommerce.com", os.environ.get("SUPERUSER_PASSWORD")),
    ],
)
def test_login_superuser_with_username_and_email(client, login_user, password):
    url = reverse("account:login")
    data = {"username": login_user, "password": password}
    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    "login_user, password",
    [
        ("mako", "Stefan13!"),
        ("mako@gmail.com", "Stefan13!"),
        ("tako", "August13!"),
        ("tako@gmail.com", "August13!"),
        ("bako", "Zygmunt13!"),
        ("bako@gmail.com", "Zygmunt13!"),
    ],
)
def test_login_users_with_username_and_email(
    client, login_user, password, custom_users
):
    url = reverse("account:login")
    data = {"username": login_user, "password": password}
    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db
def test_logout_user(client, custom_users):
    login_url = reverse("account:login")
    data = {"username": "mako", "password": "Stefan13!"}

    response = client.post(login_url, data=data)

    assert response.status_code == 302

    logout_url = reverse("account:logout")
    response = client.get(logout_url)

    assert response.status_code == 302
