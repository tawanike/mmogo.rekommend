from django.contrib import admin
from .models import Payment

# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display =('user',  'reference', 'amount', 'status',)
    search_fields = ('user__email', 'reference', 'amount', 'status', 'brand', 'cart__id')
    list_filter = ('status',)



admin.site.register(Payment, PaymentAdmin)

