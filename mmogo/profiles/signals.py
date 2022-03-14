from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from commace.contrib.shoppinglists.models import ShoppingList

@receiver(post_save, sender=User)
def save_user(sender, instance, created, **kwargs):

    if created:
        payload = {
            'title': f'{instance.first_name}\'s Registry', 
        }
        
        # Create Registry
        shoppinglist = ShoppingList.objects.create(**payload)
        shoppinglist.user.add(instance)
        