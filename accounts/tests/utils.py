from django.urls import reverse


def login_and_get_response(client, username, password, url_name, **kwargs):
    client.login(username=username, password=password)
    url = reverse(url_name, kwargs={"username": username})
    return client.post(url, **kwargs)


def assert_address_data_saved_and_displayed(
    client, user, address_data, model, response
):
    new_address = model.objects.get(account_id=user.id)

    # check if the address data is saved in the database
    for field, value in address_data.items():
        assert getattr(new_address, field) == value

    # check if the address data is present in the response context
    response_content = response.content.decode("utf-8")
    for value in address_data.values():
        assert value in response_content
