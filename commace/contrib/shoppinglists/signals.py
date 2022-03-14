from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template import Context, Engine, Context

from commace.contrib.cart.models import Cart, CartItem
from commace.contrib.shoppinglists.models import ShoppingListItem, shoppinglists_updated_gifted, Reserved
from commace.payments.models import Payment

@receiver(shoppinglists_updated_gifted, sender=Payment)
def gift_payment_received(sender, instance, created, **kwargs):
  if created:
    products = CartItem.objects.filter(cart=instance.cart)
    
    for product in products:
      if product.shoppinglist:
        gift = ShoppingListItem.objects.get(id=product.shoppinglist.id)
        gift.status = ShoppingListItem.BOUGHT
        gift.save()
        # TODO: Send email to owner of registry notifying them of the purchase


@receiver(post_save, sender=Reserved)
def reserve_product(sender, instance, created, **kwargs):
  # TODO: Add expiry date
  if created:
    gift = ShoppingListItem.objects.get(id=instance.product.id)
    gift.status = ShoppingListItem.RESERVED
    gift.assigned = instance.user
    gift.save()
