from .forms import ProductCartAddForm


def add_update_quantity_form_to_cart(cart):
    for item in cart:
        item["update_quantity_form"] = ProductCartAddForm(
            initial={"quantity": item["quantity"], "update": True}
        )
