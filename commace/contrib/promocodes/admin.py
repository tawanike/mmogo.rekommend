from django.contrib import admin
from .models import PromoCode, Redemption

class PromoCodeAdmin(admin.ModelAdmin):
    search_fields = ('code',)
    list_display = ('code', 'is_active', 'created_at',)
    list_filter = ('is_active',)

class RedemptionAdmin(admin.ModelAdmin):
    pass

admin.site.register(PromoCode, PromoCodeAdmin)
admin.site.register(Redemption, RedemptionAdmin)
