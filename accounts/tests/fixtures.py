import datetime

import pytest
from django.test import Client
from django.urls import reverse

from accounts.models import Account, User, UserShippingAddress


@pytest.fixture
def client(db):
    client = Client()
    return client


@pytest.fixture(scope="class")
def custom_users(django_db_blocker):
    with django_db_blocker.unblock():
        users = [
            User.objects.create_user(
                username="mako", email="mako@gmail.com", password="Stefan13!"
            ),
            User.objects.create_user(
                username="tako", email="tako@gmail.com", password="August13!"
            ),
            User.objects.create_user(
                username="bako", email="bako@gmail.com", password="Zygmunt13!"
            ),
        ]

        yield users


@pytest.fixture
def custom_user(db):
    custom_user = User.objects.create_user(
        username="lukasz", email="lukasz@gmail.com", password="Łukasz13!"
    )

    return custom_user


@pytest.fixture
def custom_user_with_profile(db, custom_user):
    user_profile = Account.objects.get(pk=custom_user.id)

    user_profile.first_name = "Łukasz"
    user_profile.last_name = "Krupiński"
    user_profile.date_of_birth = datetime.date(1991, 8, 24)
    user_profile.phone = "+48601945444"

    user_profile.save()

    return custom_user


@pytest.fixture
def inactive_user(db):
    inactive_user = User.objects.create_user(
        username="joanna",
        email="joanna@gmail.com",
        password="Joanna13!",
        is_active=False,
    )

    return inactive_user


@pytest.fixture
def send_request(db, client):
    def send_request(email_address=None, **kwargs):
        if email_address is not None:
            url = reverse("account:login")
            data = {"email": email_address}
        else:
            url = reverse("account:register")
            data = kwargs

        response = client.post(url, data=data, follow=True)

        return response

    return send_request


@pytest.fixture
def create_shipping_addresses(db, custom_user):
    shipping_address_data = [
        {
            "street": "Żelazna 42/5",
            "zip_code": "51-121",
            "city": "Wrocław",
            "state": "dolnośląskie",
            "country": "Polska",
            "account_id": custom_user.id,
            "first_name": "Rafał",
            "last_name": "Krupiński",
        },
        {
            "street": "Nowowiejska 9/18",
            "zip_code": "53-123",
            "city": "Wrocław",
            "state": "dolnośląskie",
            "country": "Polska",
            "account_id": custom_user.id,
            "first_name": "Maciej",
            "last_name": "Młynarski",
        },
    ]

    shipping_addresses = [UserShippingAddress(**data) for data in shipping_address_data]

    UserShippingAddress.objects.bulk_create(shipping_addresses)

    return shipping_addresses
