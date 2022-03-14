from rest_framework import generics
from rest_framework.permissions import AllowAny

from commace.products.models import Product
from commace.products.serializers import ProductSerializer
from commace.stores.models import Store
from commace.stores.serializers import StoreSerializer


class StoresAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = StoreSerializer
    queryset = Store.objects.filter(published=True)


class StoreAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = StoreSerializer
    queryset = Store.objects.filter(published=True)
    lookup_field = 'id'


class StoreProducts(generics.ListAPIView):
    serializer_class = ProductSerializer
    lookup_field = 'shop'

    def get_queryset(self):
        shop = self.kwargs['shop']
        return Product.objects.filter(published=True, shop__id=shop)


class StoreCategoryProducts(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = StoreSerializer
    queryset = Store.objects.filter(published=True)


class StoreCategories(generics.RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = StoreSerializer
    queryset = Store.objects.filter(published=True)


class FeaturedStoresAPIView(generics.ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = StoreSerializer
    queryset = Store.objects.filter(published=True, featured=True)