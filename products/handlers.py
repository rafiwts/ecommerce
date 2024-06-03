import random
import uuid
from datetime import datetime

from django.utils.text import slugify


def image_directory_path(instance, filename):
    now = datetime.now()
    full_name = f"{instance.product}-{instance.image}"
    return f"product/{instance.product_id}/{full_name}-{now}-{filename}"


def generate_product_id_handler():
    product_id = random.randint(1000000, 9999999)
    return product_id


def generate_unique_slug(model_class, name):
    slug = slugify(name)
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{slug}-{uuid.uuid4().hex[:6]}"
    return slug
