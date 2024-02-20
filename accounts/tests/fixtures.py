import pytest
from django.test import Client


@pytest.fixture
def client(db):
    client = Client()
    return client
