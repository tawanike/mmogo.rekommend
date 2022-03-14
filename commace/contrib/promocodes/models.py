from django.db import models
from django.contrib.auth.models import User


class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    value = models.DecimalField(default=0, decimal_places=2, max_digits=11)
    is_active = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    number = models.SmallIntegerField(default=0)
    per_user = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return str(self.code)
    
    class Meta:
        db_table = 'promocodes'
        verbose_name = 'Promo Code'
        verbose_name_plural = 'Promo Codes'


class Redemption(models.Model):
    user = models.ForeignKey(User, related_name="user_promocode", on_delete=models.CASCADE, blank=True, null=True)
    promocode = models.ForeignKey(PromoCode, related_name="user_redemption", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.user)
    
    class Meta:
        db_table = 'redemptions'
        verbose_name = 'Redemption'
        verbose_name_plural = 'Redemptions'
