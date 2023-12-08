import random
from datetime import datetime

from django.contrib.auth import get_user_model


def image_directory_path(instance, filename):
    now = datetime.now()
    full_name = f"{instance.first_name} {instance.last_name}"
    return f"{instance.id}-{full_name}-{now}-{filename}"


def generate_client_id():
    while True:
        client_id = random.randint(1000000, 9999999)
        if not get_user_model().objects.filter(account__client_id=client_id).exists():
            return client_id
