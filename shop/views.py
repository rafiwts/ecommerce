from django.shortcuts import render


def shop(requset):
    return render(requset, "shop/shop.html")


def sale(requset):
    return render(requset, "shop/sale.html")


def vendor(requset):
    return render(requset, "shop/vendor.html")


def info(requset):
    return render(requset, "shop/info.html")


def contact(requset):
    return render(requset, "shop/contact.html")
