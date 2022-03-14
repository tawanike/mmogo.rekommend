from django.db import models
from django.contrib.auth.models import User
from commace.contrib.cart.models import Cart

# Create your models here.
class Payment(models.Model):
    PENDING = 0
    SUCCESS = 1
    STATUS = ((PENDING, 'Pending'),
                (SUCCESS, 'Success'),)
    
    payment_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='payments_user', on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, related_name='payments_cart', on_delete=models.CASCADE, blank=True, null=True)
    reference =  models.CharField(max_length=255, unique=True, blank=True, null=True)
    service = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    fees = models.DecimalField(default=0, decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=PENDING, choices=STATUS)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    authorization = models.JSONField(null=True, blank=True)
    customer = models.JSONField(null=True, blank=True)
    log = models.JSONField(null=True, blank=True)
    source = models.JSONField(null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    gateway_response = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        db_table = 'payments'
        verbose_name =  'Payment'
        verbose_name_plural= 'Payments'

    def status_display(self):
        return self.STATUS[self.status][1]