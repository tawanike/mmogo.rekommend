from django.contrib import admin
from .models import Order, OrderStatus
# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'tracking_code', 'payment', 'is_active',)
    search_fields = ('user__email', 'tracking_code', 'payment', 'is_active',)
    list_filter = ('is_active', 'payment',)
    readonly_fields = ('created_at', 'updated_at',)

class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('order', 'status', 'driver', 'is_active',)
    search_fields = ('user__email', 'status', 'is_active',)
    list_filter = ('status', 'is_active',)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)