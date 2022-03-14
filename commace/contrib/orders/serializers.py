from datetime import datetime
from django.contrib.auth.models import User

from rest_framework import serializers

from admin import settings

from .models import Order, OrderStatus
from commace.payments.models import Payment
from commace.contrib.cart.models import Cart, CartItem
from commace.contrib.cart.serializers import CartItemSerializer, CartSerializer
from commace.payments.paystack.serializers import PaystackSerializer

from altur import Altur
from mmogo.profiles.serializers import UserSerializer
from mmogo.utils import format_mobile_number
from mmogo.contrib.addresses.models import Address
from mmogo.contrib.addresses.serializers import AddressSerializer

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    payment = PaystackSerializer()
    cart = CartSerializer()
    delivery_address = AddressSerializer()
    status = serializers.CharField(max_length=50, source='status_display')

    def create(self, validated_data):
        user = self.context['request'].user
        cart_id = validated_data['cart']
        address_id =  validated_data['delivery_address']
        cart = Cart.objects.get(id=cart_id, user=user, is_active=True)
        
        address = Address.objects.get(id=address_id, user=user)
        try:
            mobile=validated_data['mobile']
        except KeyError:
            mobile = User.objects.get(email=user).mobile
        try:
            instructions = validated_data['instructions']
        except KeyError:
            instructions = ''
        order = Order.objects.create(
            user=user, cart=cart, payment=Order.PAID, payment_reference=validated_data['payment_reference'],
            mobile=mobile, instructions=instructions, delivery_address=address, tracking_code=tracking_code
        )
        payment = Payment.objects.get(payment_reference=validated_data['payment_reference'])


        cart.is_active =  False
        cart.status = Cart.PAID
        cart.save()
        
        cart_items = CartItem.objects.filter(cart=cart)

        payload = {
                    "title": "Payment Received!",
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "order": str(order.id),
                    "email" : user.email,
                    "amount": payment.amount,
                    "subject": "Receipt for Order #{}".format(tracking_code),
                    "cart": CartItemSerializer(cart_items)
                }

        altur = Altur()
        altur.payment(payload)
        altur.send_otp({'number': format_mobile_number(order.user.mobile),
                    'message': "Thank you for placing an order with eButler. {} is your tracking code.".format(
                    tracking_code)})

        altur.send_receipt(settings.SENDGRID_INVOICE_TEMPLATE_ID, payload)

        return order

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['status', 'payment', 'is_active', 'user', 'tracking_code',]


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderStatus
        fields = ['order', 'status', 'description', 'created_at', 'updated_at', 'eta', 'is_active']
        depth = 2
