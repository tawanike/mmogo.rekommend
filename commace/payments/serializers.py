# from decimal import Decimal
# from django.db import transaction
# from rest_framework import serializers

# from mmogo.profiles.models import User
# from commace.payments.models import Payment
# from mmogo.contrib.addresses.models import Address
# from commace.payments.models import Payment
# from commace.contrib.cart.models import Cart
# from commace.contrib.shoppinglists.models import shoppinglists_updated_gifted
# from commace.contrib.orders.models import Order, OrderStatus, order_status_updated
# from sentry_sdk import capture_exception


# class PaymentSerializer(serializers.ModelSerializer): 
#     def create(self, validated_data):
#         try:
#             with transaction.atomic():
#                 data = validated_data['data']
                
#                 address = Address.objects.get(id=data['address'])

#                 cart = Cart.objects.get(id=data['cart'])
#                 cart.status = Cart.PAID
#                 cart.is_active = False
#                 cart.save()

#                 payment = Payment()
#                 # payment.source = '' TODO Specify if payment is from mobile/web/whatsapp/Vodacom/ebucks
#                 payment.cart = cart
#                 payment.payment_id = data['transaction']
#                 payment.save()

#                 # Create order
#                 address = Address.objects.get(id=data.get('address'))

#                 order = Order()
#                 order.cart = cart
#                 order.mobile = data.get('mobile')
#                 order.instructions = data.get('instructions')
#                 order.delivery_address = address
#                 order.save()                

#                 OrderStatus.objects.create(
#                     cart=cart,
#                     driver=User.objects.get(email="drivers@commace.co")
#                 )
#                 order_status_updated.send(sender=OrderStatus)
#                 shoppinglists_updated_gifted.send(sender=Cart)

#                 return payment
#         except Exception as error:
#             capture_exception(error)
#             return error


#     def update(self, instance, validated_data):
#         try:
#             data = validated_data

#             # id = self.kwargs['payment_id']

#             user = User.objects.get(email=data['customer']['email'])
#             amount = Decimal(data['amount']/100)
#             fees = Decimal(data['fees']/100)
            
#             payment = Payment()
#             payment.user = user
#             payment.payment_id = data['id']
#             payment.amount = amount
#             payment.currency = data['currency']
#             payment.reference = data['reference']
#             payment.status = Payment.SUCCESS
#             payment.service = 'PAYSTACK'
#             payment.paid_at = data['paid_at']
#             payment.ip_address = data['ip_address']
#             payment.channel = data['channel']
#             payment.domain = data['domain']
#             payment.fees = fees
#             payment.customer = data['customer']
#             payment.log = data['log']
#             payment.metadata = data['metadata']
#             payment.source = data['source']
#             payment.authorization = data['authorization']
#             payment.gateway_response = data['gateway_response']
#             payment.save()

#             # return Response({}, status=status.HTTP_200_OK)
#         except Exception as error:
#             print(error)
#     class Meta:
#         model = Payment
#         fields = '__all__'
