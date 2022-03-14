from django.contrib import admin
from .models import ShoppingListContributor, ShoppingList, ShoppingListItem, Reserved

class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'published', 'public',)
    search_fields = ('title', 'description', 'user__email')
    list_filter = ('featured', 'published', 'public',)
    readonly_fields = ('created_at', 'updated_at',)

class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('shoppinglist', 'product', 'quantity', 'user',)
    search_fields = ('shoppinglist__title', 'product__title', 'user__email')
    readonly_fields = ('created_at', 'updated_at',)

class ShoppingListContributorAdmin(admin.ModelAdmin):
    list_display = ('shoppinglist',  'invite_accepted', 'user', 'invitee',)
    search_fields = ('shoppinglist__title', 'user__email', 'invitee',)
    readonly_fields = ('created_at', 'updated_at',)

class ReservedAdmin(admin.ModelAdmin):
    list_display = ('user',  'product', 'is_expired', 'expires_at',)
    readonly_fields = ('created_at', 'updated_at',)

admin.site.register(Reserved, ReservedAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
admin.site.register(ShoppingListItem, ShoppingListItemAdmin)
admin.site.register(ShoppingListContributor, ShoppingListContributorAdmin)
