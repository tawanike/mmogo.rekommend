from django.dispatch import receiver
from django.template import Context, Engine, Context

from .models import Order, OrderStatus, order_status_updated
from .utils import create_tracking_code
from commace.payments.models import Payment
from commace.contrib.cart.models import Cart

from altur.email.models import Email

@receiver(order_status_updated, sender=OrderStatus)
def payment_received(sender, instance, created, **kwargs):

    if created:
      if instance.status == Payment.SUCCESS:
        print('Payment Received Created')
      else:
        print('HANDLE PAYMENT NOT CONFIRMED')

    if not created and instance.status == Payment.SUCCESS:
      # TODO Replace this with a simpler Util Function
      # Send email notification
      engine = Engine.get_default()
      context = Context({
          "first_name": instance.user.first_name,
          "total": instance.amount
      })
      
      template = engine.get_template('email/payment-received.html')
      context = Context(context)
      body = template.render(context)


      Email.objects.create(
          subject='Payment Received',
          from_address='jerry@ebutler.co.za',
          body=body,
          recipient=instance.user.email,
          service='SES',
      )

      # Notify Slack TODO Replace this with a simpler Util Function

      # Send SMS TODO Replace this with a simpler Util Function

      # Create order

    #   address =  validated_data['address']

    #   cart = Cart.objects.get(id=instance.cart)

    #   tracking_code = create_tracking_code()
    #   address = Address.objects.get(id=address)

    #   try:
    #       mobile=validated_data['mobile']
    #   except KeyError:
    #       mobile = User.objects.get(email=user).mobile
    #   try:
    #       instructions = validated_data['instructions']
    #   except KeyError:
    #       instructions = ''

    #   order = Order.objects.create(
    #       user=user, cart=cart, payment=Payment.PAID,
    #       mobile=mobile, instructions=instructions, 
    #       delivery_address=address, tracking_code=tracking_code
    #   )

      # TODO Update inventory levels

      # Send SMS Notification
      # Send Push Notification
      #Send Email Notification

      
      # Create an order status