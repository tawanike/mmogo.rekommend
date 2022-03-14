from rest_framework.permissions import AllowAny
from rest_framework import generics


from mmogo.contrib.categories.serializers import CategorySerializer
from mmogo.contrib.categories.models import Category
from commace.products.models import Product
from commace.products.serializers import ProductSerializer


class CategoriesAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(published=True).prefetch_related('subcategories')


class CategoryAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(published=True).prefetch_related('subcategories')
    lookup_field = 'id'


class FeaturedCategories(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(featured=True, published=True).prefetch_related('subcategories')


class SubcategoryAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        category = Category.objects.get(id=self.kwargs['id'])
        queryset = category.subcategories.all()

        return queryset


class CategoryProductsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        category = Category.objects.get(id=id)
        return Product.objects.filter(category__id__in=category.subcategories.all(), published=True)

class ParentCategories(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_parent=True, published=True).prefetch_related('subcategories')


class FeaturedCategoryProductsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        id = self.kwargs['id']
        category = Category.objects.get(id=id)
        queryset = Product.objects.filter(category__in=category.subcategories.all(), published=True)
        return queryset


class SubCategoryCategoryProducts(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        category = self.kwargs['id']
        return Product.objects.filter(category__id=category, published=True)
