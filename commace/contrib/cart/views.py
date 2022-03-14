import json
from django.contrib.contenttypes.models import ContentType

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from commace.contrib.cart.serializers import CartItemSerializer, CartSerializer
from commace.contrib.cart.models import CartItem, Cart
from commace.products.models import Product, Bundle

class CartsAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    
class CartAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_active=True)
    lookup_field = 'id'

class CartItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    lookup_field = 'id'


class UserCartAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = CartSerializer
    queryset = Cart.objects.filter(is_active=True)
    lookup_field = 'user'

    def get(self, request, user):
        try:
            queryset = Cart.objects.get(is_active=True, user__id=user)
        except Cart.DoesNotExist:
            queryset = Cart.objects.create(user=request.user)

        serializer = CartSerializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)