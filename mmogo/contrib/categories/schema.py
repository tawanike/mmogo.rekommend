import graphene
from graphene_django import DjangoObjectType

from mmogo.contrib.categories.models import Category

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "title", "parent")

class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)
    category = graphene.Field(CategoryType, title=graphene.String(required=True))

    def resolve_categories(root, info):
        # We can easily optimize query count in the resolve method
        return Category.objects.select_related("subcategories").all()

    def resolve_category(root, info, title):
        try:
            return Category.objects.get(title=title)
        except Category.DoesNotExist:
            return None

# schema = graphene.Schema(query=Query)