from haystack import indexes

from .models import Product


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    # Define the document field
    text = indexes.CharField(document=True, use_template=True)

    # Other fields can be defined as needed
    name = indexes.CharField(model_attr="name", boost=1.5)
    description = indexes.CharField(model_attr="description")

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
