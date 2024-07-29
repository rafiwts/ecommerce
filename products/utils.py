import json
import random


def handle_last_seen_products(request, product_id=False):
    """
    Returns last seen products from cookies and if
    the new product is seen and is not in a list
    already it adds to a context
    """
    last_seen_products = request.COOKIES.get("last_seen_products", "[]")
    last_seen_products = json.loads(last_seen_products)

    if product_id:
        if product_id not in last_seen_products:
            last_seen_products.append(product_id)

    # remember only 8 last seen products
    if len(last_seen_products) > 8:
        last_seen_products.pop(0)

    return last_seen_products


def get_random_sample(products, sample_size):
    return random.sample(products, min(sample_size, len(products)))


def get_recommendations(last_seen_products, favorite_products, sample_size=8):
    # set to avoid duplicates
    combined_products = list(set(last_seen_products) | set(favorite_products))
    return get_random_sample(combined_products, sample_size)
