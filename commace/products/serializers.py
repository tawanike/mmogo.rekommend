from rest_framework import serializers

from commace.contrib.brands.serializers import BrandSerializer
from commace.stores.serializers import StoreSerializer
from mmogo.contrib.categories.serializers import CategorySerializer
from mmogo.contrib.medialibrary.serializers import AltMediaLibrarySerializer
from .models import Product, ProductVariation, Bundle


class ProductSerializer(serializers.ModelSerializer):
    shop = StoreSerializer()
    brand = BrandSerializer()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = "__all__"

class ProductVariationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariation
        fields = "__all__"

class AltProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ('id', 'title', 'description', 'image', 'cover', 'price', 'promo_price', 
                    'size', 'cost', 'height', 'width',)

class AltProductSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField('title', read_only=True)
    category = serializers.SlugRelatedField('title', read_only=True)
    images = AltMediaLibrarySerializer(many=True)
    variations = AltProductVariationSerializer(many=True)
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'image', 'cover', 'price', 'promo_price', 'unit_of_measure',
                    'size', 'tags', 'height', 'width', 'cost', 'brand', 'category', 'images', 'variations',)

class BundleSerializer(serializers.ModelSerializer):
    shop = StoreSerializer()
    brand = BrandSerializer()
    category = CategorySerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Bundle
        fields = "__all__"
