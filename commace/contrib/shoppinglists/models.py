from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from commace.products.models import Product

shoppinglists_updated_gifted = Signal()

class ShoppingList(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='shoppinglists/', blank=True, null=True)
    cover = models.ImageField(
        upload_to='shoppinglists/covers/', blank=True, null=True)
    ordering = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    user = models.ManyToManyField(User, through=u'ShoppingListContributor', related_name='listcontributor')
    published = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=6, blank=True, null=True)
    show_on_profile = models.BooleanField(default=False)
    class Meta:
        db_table = 'shoppinglists'
        ordering = ['ordering','title',]
        verbose_name = 'Registry'
        verbose_name_plural = 'Registries'

    def __str__(self) -> str:
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Make sure slug is unique
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class ShoppingListItem(models.Model):
    AVAILABLE = 0
    RESERVED = 1
    BOUGHT = 2

    ITEM_STATUS_CHOICES = (
        (AVAILABLE, 'Available'),
        (RESERVED, 'Reserved'),
        (BOUGHT, 'Bought'),
    )
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    EMERGENCY = 3

    ITEM_PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (EMERGENCY, 'Emergency'),
    )

    shoppinglist = models.ForeignKey(ShoppingList, related_name='shoppinglists', on_delete=models.CASCADE )
    product = models.ForeignKey(Product, related_name='products', on_delete=models.CASCADE)
    ordering = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE) # TODO related through
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.PositiveSmallIntegerField(default=AVAILABLE, choices=ITEM_STATUS_CHOICES)
    priority = models.PositiveSmallIntegerField(default=LOW, choices=ITEM_PRIORITY_CHOICES)
    assigned = models.ForeignKey(User, related_name='assigned', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'shoppinglists_items'
        ordering = ['shoppinglist',]
        verbose_name = 'Registry Item'
        verbose_name_plural = 'Registry Items'

    def __str__(self) -> str:
        return f'{self.product} - {self.shoppinglist}'

    def priority_display(self):
        return self.ITEM_PRIORITY_CHOICES[self.priority][1]

    def status_display(self):
        return self.ITEM_STATUS_CHOICES[self.status][1]

class ShoppingListContributor(models.Model):
    shoppinglist  = models.ForeignKey(ShoppingList, related_name='shoppinglist_parent', on_delete=models.CASCADE )
    user = models.ForeignKey(User, related_name='shoppinglist_invitee', on_delete=models.CASCADE)
    invitee = models.CharField(max_length=255, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    invite_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shoppinglists_contributors'
        ordering = ['shoppinglist',]
        verbose_name = 'Registry Contributor'
        verbose_name_plural = 'Registry Contributors'

    def __str__(self) -> str:
        return str(self.shoppinglist)

class Reserved(models.Model):
    user = models.ForeignKey(User, related_name='user_reserves', on_delete=models.CASCADE)
    product  = models.ForeignKey(ShoppingListItem, related_name='reserved_products', on_delete=models.CASCADE )
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'gift_reservations'
        ordering = ['created_at',]
        verbose_name = 'Reserved Product'
        verbose_name_plural = 'Reserved Products'

    def __str__(self) -> str:
        return str(self.product)
