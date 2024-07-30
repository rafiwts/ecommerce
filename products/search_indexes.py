from haystack import indexes

from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name", boost=1.5)
    description = indexes.CharField(model_attr="description")

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
