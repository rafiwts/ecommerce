import random
from datetime import datetime


def image_directory_path(instance, filename):
    now = datetime.now()
    full_name = f"{instance.category}-{instance.name}"
    return f"product/{instance.product_id}-{full_name}-{now}-{filename}"


def generate_product_id_handler():
    product_id = random.randint(1000000, 9999999)
    return product_id
