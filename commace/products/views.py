from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import AllowAny

from commace.products.models import Product, Bundle
from commace.products.serializers import ProductSerializer, BundleSerializer


class ProductsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(published=True)


class ProductsTitleAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(published=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['@title']

class ProductsBarcodeAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(published=True)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=barcode']


class ProductAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return Product.objects.filter(id=id, published=True)


class FeaturedProductAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(published=True, featured=True)


class DealsAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(featured=True, published=True)

class BundlesAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BundleSerializer
    queryset = Bundle.objects.filter(published=True)


class BundleAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BundleSerializer
    lookup_field = 'id'

    def get_queryset(self):
        id = self.kwargs['id']
        return Bundle.objects.filter(id=id, published=True)


class FeaturedBundlesAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BundleSerializer
    queryset = Bundle.objects.filter(published=True, featured=True)

