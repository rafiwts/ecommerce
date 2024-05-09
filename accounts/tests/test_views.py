import datetime
import os

import pytest
from django.urls import reverse
from dotenv import load_dotenv
from freezegun import freeze_time

from accounts.models import ResetPasswordLink, User

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
    "username, password",
    [
        ("mako", "Stefan13!"),
        ("tako", "August13!"),
        ("bako", "Zygmunt13!"),
    ],
)
def test_login_users_with_username(client, username, password, custom_users):
    url = reverse("account:login")
    data = {"username": username, "password": password}
    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email, password",
    [
        ("mako@gmail.com", "Stefan13!"),
        ("tako@gmail.com", "August13!"),
        ("bako@gmail.com", "Zygmunt13!"),
    ],
)
def test_login_users_with_email(client, email, password, custom_users):
    url = reverse("account:login")
    data = {"username": email, "password": password}
    response = client.post(url, data=data)

    assert response.status_code == 302


@pytest.mark.django_db  # Add a test for inactive user - create him
def test_login_with_invalid_credentials(client):
    mock_username = "MockUsername"
    mock_password = "MockPassword12!"

    url = reverse("account:login")
    data = {"username": mock_username, "password": mock_password}

    response = client.post(url, data=data, follow=True)

    # TODO: Try to do it with message in a session
    assert "Invalid credentials. Try again!" in response.content.decode("utf-8")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_with_inactive_user(client, inactive_user):
    url = reverse("account:login")
    data = {"username": "joanna", "password": "Joanna13!"}

    response = client.post(url, data=data, follow=True)

    assert (
        "The account is inactive. Please contact our support!"
        in response.content.decode("utf-8")
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout_user(client, custom_users):
    login_url = reverse("account:login")
    data = {"username": "mako", "password": "Stefan13!"}

    response = client.post(login_url, data=data)

    assert response.status_code == 302

    logout_url = reverse("account:logout")
    response = client.get(logout_url)

    assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    "email",
    [
        ("mako@gmail.com"),
        ("tako@gmail.com"),
        ("bako@gmail.com"),
    ],
)
def test_reset_password_with_correct_email(client, email, custom_users):
    url = reverse("account:login")
    data = {"email": email}

    response = client.post(url, data=data, follow=True)

    assert "Password reset email sent. Check your inbox." in response.content.decode(
        "utf-8"
    )
    assert response.status_code == 200


@pytest.mark.django_db
def test_reset_password_with_incorrect_email(client):
    mock_email = "rafiwts@gmail.com"

    url = reverse("account:login")
    data = {"email": mock_email}

    response = client.post(url, data=data, follow=True)

    assert "User with his email address not found!" in response.content.decode("utf-8")
    assert response.status_code == 200


@pytest.mark.django_db
@freeze_time("2024-04-08 20:00:00")
@pytest.mark.parametrize(
    "email",
    [
        ("mako@gmail.com"),
        ("tako@gmail.com"),
        ("bako@gmail.com"),
    ],
)
def test_reset_password_link_access(
    client, email, custom_users, send_password_reset_request
):
    # get user with given email
    user = User.objects.get(email=email)

    # the amount of links before sending a password reset
    initial_link_count = ResetPasswordLink.objects.count()

    send_password_reset_request(email)

    # verify that a new link has been created
    assert ResetPasswordLink.objects.count() == initial_link_count + 1

    # verify that the link is associated with the correct user
    reset_link = ResetPasswordLink.objects.filter(user_id=user.id).first()
    assert reset_link is not None


@pytest.mark.django_db
@freeze_time("2024-04-08 20:00:00")
@pytest.mark.parametrize(
    "email",
    [
        ("mako@gmail.com"),
        ("tako@gmail.com"),
        ("bako@gmail.com"),
    ],
)
def test_reset_password_link_expiration_time(
    client, email, custom_users, send_password_reset_request
):
    # get user with given email
    user = User.objects.get(email=email)
    send_password_reset_request(email)

    reset_link = ResetPasswordLink.objects.filter(user_id=user.id).first()

    # verify that the link can be accessed
    reset_response = client.get(reset_link.link)
    assert reset_response.status_code == 200
    assert reset_link.created_at == datetime.datetime(
        2024, 4, 8, 20, 0, tzinfo=datetime.timezone.utc
    )

    # try to access the link after expiration
    expired_time = reset_link.created_at + datetime.timedelta(seconds=86400)
    with freeze_time(expired_time):
        expired_link_response = client.get(reset_link.link)

    assert expired_link_response.status_code == 404
    assert (
        expired_link_response.content.decode("utf-8") == "Link does not exist anymore"
    )
