import datetime
import os

import pytest
from django.urls import reverse
from dotenv import load_dotenv
from freezegun import freeze_time
from utils import assert_address_data_saved_and_displayed, login_and_get_response

from accounts.models import (
    Account,
    ResetPasswordLink,
    User,
    UserAddress,
    UserShippingAddress,
)

load_dotenv()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "template_name",
    {
        "home",
        "account:register",
        "account:login",
    },
)
def test_views_with_no_login_required(client, template_name):
    url = reverse(template_name)
    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
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
    client, template_name, login_user, password, custom_users
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
def test_logout_user(client):
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
def test_reset_password_with_correct_email(client, email):
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
@pytest.mark.parametrize(
    "email",
    [
        ("mako@gmail.com"),
        ("tako@gmail.com"),
        ("bako@gmail.com"),
    ],
)
def test_reset_password_link_access(client, email, send_request):
    # get user with given email
    user = User.objects.get(email=email)

    # the amount of links before sending a password reset
    initial_link_count = ResetPasswordLink.objects.count()

    send_request(email)

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
def test_reset_password_link_expiration_time(client, email, send_request):
    # get user with given email
    user = User.objects.get(email=email)
    send_request(email)

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


@pytest.mark.django_db
def test_reset_password_link_with_correct_credentials(
    client, custom_user, send_request
):
    user = User.objects.get(email=custom_user.email)
    mock_password = "Nowehasło1!"
    send_request(custom_user.email)

    reset_link = ResetPasswordLink.objects.filter(user_id=user.id).first()

    # verify that the link can be accessed
    reset_response = client.post(
        reset_link.link,
        data={"new_password": mock_password, "confirm_password": mock_password},
        follow=True,
    )

    assert reset_response.status_code == 200
    assert "Password has been changed." in reset_response.content.decode("utf-8")

    # login with new credentials
    login_url = reverse("account:login")
    data = {"username": custom_user.username, "password": mock_password}

    login_response = client.post(login_url, data)

    assert login_response.status_code == 302


@pytest.mark.django_db
@pytest.mark.parametrize(
    "new_password, confirm_password, error_message",
    [
        ("NoDigit", "NoDigit", "New password must contain at least one digit."),
        (
            "noupper1",
            "noupper1",
            "New password must contain at least one uppercase letter.",
        ),
        (
            "nodigitandupper",
            "nodigitandupper",
            "New password must contain at least one uppercase letter and one digit.",
        ),
        ("Different1", "Different2", "Passwords do not match."),
    ],
)
def test_reset_password_link_with_incorrect_credentials(
    client, custom_user, send_request, new_password, confirm_password, error_message
):
    user = User.objects.get(email=custom_user.email)
    send_request(custom_user.email)

    reset_link = ResetPasswordLink.objects.filter(user_id=user.id).first()

    # verify that the link cannot be accessed due to invalid credentials
    reset_response = client.post(
        reset_link.link,
        data={"new_password": new_password, "confirm_password": confirm_password},
        follow=True,
    )

    assert reset_response.status_code == 200
    assert error_message in reset_response.content.decode("utf-8")


@pytest.mark.django_db
def test_register_user_correct_data(client, send_request):
    user_data = {
        "username": "makoboss",
        "email": "makobossss@gmail.com",
        "password1": "Django12",
        "password2": "Django12",
    }

    # create a user
    send_request(**user_data)

    profile_data = {
        "first_name": "Maciej",
        "last_name": "Młynarski",
        "date_of_birth": datetime.date(1995, 4, 8),
        "phone_0": "PL",
        "phone_1": "602421032",
    }

    # create a profile with profile data
    url = reverse("account:create-profile")
    response = client.post(url, data=profile_data, follow=True)

    assert response.status_code == 200

    # get a created user
    new_user = User.objects.select_related("account").get(
        username=user_data["username"]
    )

    assert new_user.is_active == True  # noqa: E712
    assert new_user.is_authenticated == True  # noqa: E712
    assert new_user.email == user_data["email"]
    assert new_user.account.first_name == profile_data["first_name"]
    assert new_user.account.last_name == profile_data["last_name"]
    assert profile_data["phone_1"] in str(new_user.account.phone)
    assert new_user.account.date_of_birth == profile_data["date_of_birth"]

    # login a user
    url = reverse("account:login")
    response = client.post(
        url,
        data={"username": user_data["username"], "password": user_data["password1"]},
    )

    assert response.status_code == 302


# TODO: add more examples for this test
@pytest.mark.django_db
@pytest.mark.parametrize(
    "username, email, password1, password2, error_message",
    [
        (
            "lukasz",
            "wybierz@gmail.com",
            "Cotam123",
            "Cotam123",
            "The username lukasz already exists.",
        ),
        (
            "username",
            "lukasz@gmail.com",
            "Cotam123",
            "Cotam123",
            "The email lukasz@gmail.com already exists.",
        ),
    ],
)
def test_user_existence_when_registering(
    client,
    custom_user,
    send_request,
    username,
    email,
    password1,
    password2,
    error_message,
):
    data = {
        "username": username,
        "email": email,
        "password1": password1,
        "password2": password2,
    }

    url = reverse("account:register")

    response = client.post(url, data=data, follow=True)

    assert error_message in response.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_view_personal_data_display(client, custom_user_with_profile):
    updated_user = User.objects.select_related("account").get(
        username=custom_user_with_profile.username
    )

    # login and go to edit profile
    client.login(username=custom_user_with_profile.username, password="Łukasz13!")
    edit_profile_url = reverse(
        "account:profile-view", kwargs={"username": custom_user_with_profile.username}
    )
    edit_profile_response = client.get(edit_profile_url)

    assert updated_user.username in edit_profile_response.content.decode("utf-8")
    assert updated_user.email in edit_profile_response.content.decode("utf-8")
    assert updated_user.account.first_name in edit_profile_response.content.decode(
        "utf-8"
    )
    assert updated_user.account.last_name in edit_profile_response.content.decode(
        "utf-8"
    )
    assert "+48601945444" in edit_profile_response.content.decode("utf-8")


@pytest.mark.django_db
def test_profile_view_personal_data_edit(client, custom_user_with_profile):
    new_profile_data = {
        "first_name": "Roman",
        "last_name": "Adamczyk",
        "date_of_birth": datetime.date(2000, 2, 2),
        "phone_0": "PL",
        "phone_1": "602322032",
    }

    # login and go to edit profile
    edit_profile_response = login_and_get_response(
        client,
        custom_user_with_profile.username,
        "Łukasz13!",
        "account:edit-account",
        data=new_profile_data,
        follow=True,
    )
    updated_profile = Account.objects.get(user_id=custom_user_with_profile.id)

    # check if data has been saved to a database
    assert new_profile_data["first_name"] == updated_profile.first_name
    assert new_profile_data["last_name"] == updated_profile.last_name
    assert new_profile_data["date_of_birth"] == updated_profile.date_of_birth
    assert "+48602322032" == updated_profile.phone

    # check if data display on page
    assert new_profile_data["first_name"] in edit_profile_response.content.decode(
        "utf-8"
    )
    assert new_profile_data["last_name"] in edit_profile_response.content.decode(
        "utf-8"
    )
    assert "Feb. 2, 2000" in edit_profile_response.content.decode("utf-8")
    assert "+48602322032" in edit_profile_response.content.decode("utf-8")


address_data = {
    "street": "Modra 42/5",
    "zip_code": "54-151",
    "city": "Wrocław",
    "state": "dolnośląskie",
    "country": "Polska",
}


@pytest.mark.django_db
def test_profile_view_home_address_edit(client, custom_user):
    # login and go to edit address
    edit_address_response = login_and_get_response(
        client,
        custom_user.username,
        "Łukasz13!",
        "account:edit-address",
        data=address_data,
        follow=True,
    )

    assert_address_data_saved_and_displayed(
        client, custom_user, address_data, UserAddress, edit_address_response
    )


@pytest.mark.django_db
def test_profile_view_new_shipping_address_add(client, custom_user):
    shipping_address_data = address_data
    shipping_address_data["first_name"] = "Marek"
    shipping_address_data["last_name"] = "Podolski"

    # login and go to edit shipping address
    add_shipping_address_response = login_and_get_response(
        client,
        custom_user.username,
        "Łukasz13!",
        "account:shipping-address-add",
        data=shipping_address_data,
        follow=True,
    )

    assert_address_data_saved_and_displayed(
        client,
        custom_user,
        shipping_address_data,
        UserShippingAddress,
        add_shipping_address_response,
    )


@pytest.mark.django_db
def test_profile_view_shipping_address_delete(client, create_shipping_addresses):
    user = User.objects.get(id=2)

    assert UserShippingAddress.objects.count() == 2

    client.login(username=user.username, password="Łukasz13!")
    url = reverse(
        "account:delete-shipping-address",
        kwargs={"username": user.username, "address_id": 2},
    )
    client.post(url, follow=True)

    assert UserShippingAddress.objects.count() == 1


shipping_address_data = [
    {
        "street": "Brajana 21/1",
        "zip_code": "54-321",
        "city": "Brzeg",
        "state": "dolnośląskie",
        "country": "Polska",
        "first_name": "Piotr",
        "last_name": "Grzegorzek",
    },
    {
        "street": "Małpia 2/28",
        "zip_code": "05-233",
        "city": "Sosnowiec",
        "state": "śląskie",
        "country": "Polska",
        "first_name": "Tomek",
        "last_name": "Borek",
    },
]


@pytest.mark.django_db
def test_profile_view_shipping_address_edit(client, create_shipping_addresses):
    user = User.objects.get(id=2)

    client.login(username=user.username, password="Łukasz13!")

    for index, address_data in enumerate(shipping_address_data, start=1):
        url = reverse(
            "account:update-shipping-address",
            kwargs={"username": user.username, "address_id": index},
        )
        response = client.post(url, data=address_data, follow=True)
        updated_shipping_address = UserShippingAddress.objects.get(id=index)

        # Check if database was updated
        for key, value in address_data.items():
            assert getattr(updated_shipping_address, key) == value

        # Check if new address is displayed
        for key, value in address_data.items():
            assert value in response.content.decode("utf-8")
