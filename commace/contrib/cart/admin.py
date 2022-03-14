from django.contrib import admin
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'contacted', 'is_active',)
    search_fields = ('user', 'status', 'contacted', 'is_active',)
    list_filter = ('contacted', 'is_active', 'status',)
    readonly_fields = ('created_at', 'updated_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'user', 'status', 'quantity', 'price',)
    search_fields = ('cart', 'user', 'status', 'quantity', 'price',)
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
