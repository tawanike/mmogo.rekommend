from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import User


from commace.contrib.cart.models import Cart
from commace.payments.models import Payment
from mmogo.contrib.addresses.models import Address
# Create your models here.

order_status_updated = Signal()


class Order(models.Model):
    PAYMENT_PENDING = 0
    PAID = 1
    DECLINED = 2
    REFUNDED = 3

    PAYMENT = (
        (PAYMENT_PENDING, 'Payment Pending'),
        (PAID,'Paid'), 
        (DECLINED, 'Declined'), 
        (REFUNDED, 'Refunded')
    )
                
    cart = models.ForeignKey(Cart, related_name='order_cart', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, related_name='order_user', on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, related_name='order_address', on_delete=models.CASCADE)
    tracking_code=models.CharField(max_length=6, unique=True)
    status = models.IntegerField(default=PAYMENT_PENDING, choices=PAYMENT)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.tracking_code)
    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def status_display(self):
        return self.PAYMENT[self.status][1]

class OrderStatus(models.Model):
    RECEIVED = 0
    PROCESSING = 1
    DELIVERED = 2

    ORDER_STATUS = (
        (RECEIVED, 'Order Received'),
        (PROCESSING,'Processing Order'),
        (DELIVERED, 'Order Delivered'), 
    )

    order = models.ForeignKey(Order, related_name='order_status', on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name='dispacher', on_delete=models.CASCADE)
    status = models.IntegerField(default=RECEIVED, choices=ORDER_STATUS)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    eta = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    # TODO Updated by


    def __str__(self):
        return str(self.order.tracking_code)
    class Meta:
        db_table = 'order_status'
        verbose_name = 'Order Status'
        verbose_name_plural = 'Order Status'


    def status_display(self):
        return self.ORDER_STATUS[self.status][1]