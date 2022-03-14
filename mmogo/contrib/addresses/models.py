from django.db import models
from django.contrib.auth.models import User

from mmogo.contrib.locations.models import Country

class Address(models.Model):
    user = models.ForeignKey(User,related_name='user_address', on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=10, blank=True, null=True)
    complex_name = models.CharField(max_length=255, blank=True, null=True)
    street_address = models.CharField(max_length=255)
    suburb = models.CharField(max_length=255, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    city = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255)
    country = models.ForeignKey(Country, related_name='country_address', on_delete=models.CASCADE)
    postcode = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, blank=True, null=True)
    formatted_address = models.TextField(max_length=255, blank=True, null=True)
    location = models.JSONField(blank=True, null=True)
    nearest_warehouse = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'addresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self) -> str:
        return str(self.street_address)

    

