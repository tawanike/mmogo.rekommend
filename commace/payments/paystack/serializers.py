from datetime import datetime
from django.db import transaction

from sentry_sdk import capture_exception
from rest_framework import serializers

from mmogo.profiles.models import User
from mmogo.contrib.addresses.models import Address

from commace.payments.models import Payment
from commace.contrib.cart.models import Cart
from commace.contrib.shoppinglists.models import shoppinglists_updated_gifted
from commace.contrib.orders.models import Order, OrderStatus, order_status_updated
from commace.contrib.orders.utils import create_tracking_code

class PaystackSerializer(serializers.Serializer):
    address = serializers.IntegerField(write_only=True)
    cart = serializers.IntegerField(write_only=True)
    transaction = serializers.IntegerField(write_only=True)
    status = serializers.CharField(max_length=50, source='display_status', read_only=True)
 
    def create(self, validated_data):
        print('PaystackSerializer')
        try:
            with transaction.atomic():
                data = validated_data
                address = Address.objects.get(id=data['address'])

                cart = Cart.objects.get(id=data['cart'])
                cart.status = Cart.PAID
                cart.is_active = False
                cart.save()

                payment = Payment()
                # payment.source = '' TODO Specify if payment is from mobile/web/whatsapp/Vodacom/ebucks
                payment.cart = cart
                payment.user = cart.user
                payment.payment_id = data['transaction']
                payment.paid_at = datetime.now()
                payment.save()

                # Create order
                address = Address.objects.get(id=data.get('address'))

                order = Order()
                order.cart = cart
                order.payment = payment
                order.user = cart.user
                order.tracking_code = create_tracking_code()
                # order.mobile = data.get('mobile')
                # order.instructions = data.get('instructions')
                order.delivery_address = address
                order.save()

                OrderStatus.objects.create(
                    order=order,
                    driver=User.objects.get(email="tawanda@mmogomedia.com")
                )
                order_status_updated.send(sender=OrderStatus, instance=payment, created=True)
                shoppinglists_updated_gifted.send(sender=Payment, instance=payment, created=True)

                return payment
        except Exception as error:
            print(error)

    def update(self, instance, validated_data):
        try:
            data = validated_data
            # id = self.kwargs['payment_id']

            # cart = Cart.objects.get(id=request.data.get('cart'))
            # cart.status = Cart.PAID
            # cart.is_active = False
            # cart.save()

            # payment = Payment.objects.get(payment_id=id)
            # # payment.source = '' TODO Specify if payment is from mobile/web/whatsapp/Vodacom/ebucks
            # payment.cart = cart
            # payment.save()

            # # Create order
            # address = Address.objects.get(id=data.get('address'))

            # order = Order.objects.get()
            # order.mobile = data.get('mobile')
            # order.instructions = data.get('instructions')
            # order.delivery_address = address
            # order.save()

            # return Response({}, status=status.HTTP_200_OK)
        except Exception as error:
            print('UPDATE', error)
    class Meta:
        model = Payment
        fields = '__all__'
