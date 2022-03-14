import graphene
from graphene_django import DjangoObjectType

from commace.products.models import Product
from commace.contrib.categories.schema import CategoryType


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "title", "description", "category", "image", "price", "promo_price")

class Query(graphene.ObjectType):
    products = graphene.List(ProductType)
    product = graphene.Field(CategoryType, name=graphene.String(required=True))

    def resolve_products(root, info):
        # We can easily optimize query count in the resolve method
        return Product.objects.select_related("category").all()

    def resolve_product(root, info, slug):
        try:
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None

# schema = graphene.Schema(query=Query)