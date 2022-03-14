from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from .models import Cart, CartItem

from commace.contrib.shoppinglists.models import ShoppingListItem
from commace.products.serializers import ProductSerializer, BundleSerializer
from commace.products.models import Product, Bundle
from commace.contrib.shoppinglists.serializers import ShoppingListItemSerializer


def get_product_price(product):
    if product.promo_price is not None:
        return product.promo_price
    else:
        return product.price

def get_content_type(content_type):
    if content_type == 'bundle':
        return ContentType.objects.get_for_model(Bundle)
    else:
        return ContentType.objects.get_for_model(Product)

class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(write_only=True)
    cart = serializers.IntegerField(write_only=True)
    user = serializers.IntegerField(write_only=True)
    content_type = serializers.CharField(max_length=20, write_only=True)

    def to_representation(self, instance):
        representation = super(CartItemSerializer, self).to_representation(instance)
        representation['product'] = ProductSerializer(Product.objects.select_related('shop', 'category', 'brand').get(id=instance.object_id)).data
        if instance.shoppinglist:
            representation['shoppinglist'] = ShoppingListItemSerializer(
                ShoppingListItem.objects.select_related('shoppinglist', 'user', 'product', 'assigned', 'product__category').prefetch_related('product__images').get(id=instance.shoppinglist.id)
            ).data
        return representation


    def update(self, instance, validated_data):
        quantity = validated_data['quantity']

        try:
            item = CartItem.objects.get(id=validated_data['product'])
            if quantity > 0:
                item.quantity = quantity
                item.save()
                return item
            else:
                item.delete()
                return item
        except Exception as error:
            print(error)
            return error


    def create(self, validated_data):
        user = get_object_or_404(User, id=validated_data['user'])
        product  = get_object_or_404(Product, id=validated_data['product'])
        cart = get_object_or_404(Cart, id=validated_data['cart'])
        # shoppinglist = get_object_or_404(ShoppingListItem, id=validated_data['shoppinglist'])
        
        try:
            item = CartItem.objects.get(
                cart__id=validated_data['cart'],
                object_id=validated_data['product'],
                content_type=get_content_type(validated_data['content_type'])
            )
            item.quantity += 1
            item.save()
        except CartItem.DoesNotExist:
            if validated_data.get('shoppinglist'):
                shoppinglist = validated_data['shoppinglist']
            else:
                shoppinglist = None

            item = CartItem.objects.create(
                cart=cart,
                user=user, 
                content_object=product,
                price=get_product_price(product),
                quantity=1,
                shoppinglist=shoppinglist
            )
        
        return item


    class Meta:
        model = CartItem
        fields = ('id', 'price', 'quantity', 'status', 'product', 'cart', 'user', 'content_type', 'shoppinglist')
        read_only_fields = ['status', 'price']


class CartSerializer(serializers.ModelSerializer):
    products = CartItemSerializer(many=True, read_only=True, source="cart_items")
    service_fee = serializers.DecimalField(max_digits=4, decimal_places=2, default=Decimal.from_float(settings.SERVICE_FEE))

    # def to_representation(self, instance):
    #     representation = super(CartSerializer, self).to_representation(instance)
    #     print('representation', instance.total)
    #     representation['total'] = instance.total
    #     return representation
    class Meta:
        model = Cart
        fields = ('id', 'status', 'is_active', 'discount', 'total', 'service_fee', 'subtotal', 'products')
        read_only_fields = ['products', 'service_fee']
