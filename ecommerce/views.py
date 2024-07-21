from django.shortcuts import render

from products.models import Category


def home(request):
    categories = Category.objects.all()

    return render(request, "base.html", context={"categories": categories})
