from rest_framework import generics
from rest_framework.permissions import AllowAny

from commace.contrib.brands.models import Brand
from commace.contrib.brands.serializers import BrandSerializer
from commace.products.models import Product
from commace.products.serializers import ProductSerializer

class BrandsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BrandSerializer
    queryset = Brand.objects.filter(published=True)


class BrandAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BrandSerializer
    queryset = Brand.objects.filter(published=True)
    lookup_field = 'id'


class FeaturedBrandsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BrandSerializer
    queryset = Brand.objects.filter(featured=True, published=True)


class BrandProductsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(featured=True, published=True)
    lookup_field = 'brand'

    def get_queryset(self):
        brand = self.kwargs['brand']
        return Product.objects.filter(published=True, brand__id=brand)
