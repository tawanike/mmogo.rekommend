from decimal import Decimal
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from commace.products.models import Product
from commace.contrib.promocodes.models import Redemption
from commace.contrib.shoppinglists.models import ShoppingListItem

class Cart(models.Model):
    PENDING         = 0
    CHECKOUT_PAGE   = 1
    ADDRESS_PAGE    = 2
    PAYMENT_PENDING = 3
    PAID            = 4
    
    CART_STATUS = ( (PENDING, 'Pending'),
        (CHECKOUT_PAGE, 'Checkout Page'),
        (ADDRESS_PAGE, 'Address Page'),
        (PAYMENT_PENDING, 'Payment Pending'),
        (PAID,'Paid'),
    )
    user        = models.ForeignKey(User, related_name='cart_user', on_delete=models.CASCADE)
    status      =  models.IntegerField(choices=CART_STATUS, default=PENDING)
    is_active   = models.BooleanField(default=True)
    contacted   = models.BooleanField(default=False)
    discount    = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    promocode = models.ForeignKey(Redemption, related_name='promocodes', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart'
        ordering = ['user',]
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self) -> str:
        return str(self.user)

    @property
    def total(self) -> Decimal:
        return self.subtotal  - self.discount + Decimal.from_float(settings.SERVICE_FEE)
    
    @property
    def subtotal(self) -> Decimal:
        cart_items = self.cart_items.select_related('promocode', 'cart').all()
        cart_items_total = sum(item.item_total for item in cart_items)
        return cart_items_total

    @property
    def discount(self) -> Decimal:
        cart_items = self.cart_items.select_related('promocode', 'cart').all()
        cart_items_total_discount = sum(item.discount for item in cart_items)
        
        if self.promocode:
            return self.promocode.promocode.value + Decimal.from_float(cart_items_total_discount)
        else:
            return Decimal.from_float(cart_items_total_discount)
    
class CartItem(models.Model):
    PENDING = 0
    PICKED = 1
    OUT_OF_STOCK = 2
    ALT_PICKED = 3
    CART_ITEM_STATUS = ((PENDING, 'Pending'),
        (PICKED, 'Picked'),
        (OUT_OF_STOCK, 'Out of Stock'),
        (ALT_PICKED, 'Alternative Picked')
    )
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    shoppinglist = models.ForeignKey(ShoppingListItem, related_name='gifts', null=True, blank=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    user =  models.ForeignKey(User, related_name='cart_item_user', on_delete=models.CASCADE)
    price= models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    quantity = models.IntegerField(default=0)
    status  =  models.IntegerField(choices=CART_ITEM_STATUS, default=PENDING)
    alt_product =  models.ForeignKey(Product, related_name='cart_item_alt_product',
                 on_delete=models.CASCADE, blank=True, null=True)
    alt_product_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00, blank=True, null=True)
    alt_product_quantity = models.IntegerField(default=0, blank=True, null=True)
    alt_product_status = models.IntegerField(choices=CART_ITEM_STATUS, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    promocode = models.ForeignKey(Redemption, related_name='product_promocodes', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cart_item'
        ordering = ['cart',]
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return str(self.cart)

    @property
    def discount(self):
        if self.promocode:
            return self.promocode.promocode.value
        else:
            return 0.00
   
    @property
    def item_subtotal(self):
        if self.content_object.promo_price:
            return self.content_object.promo_price * self.quantity
        else:
            return self.content_object.price * self.quantity
    
    @property
    def item_total(self):
        return self.item_subtotal - Decimal.from_float(self.discount)
