from .models import Category, Product


def categories_processor(request):
    categories = Category.objects.all()

    if request.user:
        favorite_count = Product.objects.filter(
            favoriteproduct__user=request.user
        ).count()

    context = {"categories": categories, "favorite_count": favorite_count}

    return context
