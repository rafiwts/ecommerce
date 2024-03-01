import pytest
from django.test import Client

from accounts.models import User


@pytest.fixture(scope="session")
def custom_users(django_db_setup, django_db_blocker):
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
def client(db):
    client = Client()
    return client
