from django.contrib import admin
from .models import *

class AddressAdmin(admin.ModelAdmin):
    search_fields = ('complex_name',"street_address", "city", 'user__email', 'postcode', 'municipality', )
    list_display = ('user', 'formatted_address',)
    list_filter = ('is_default',)


admin.site.register(Address, AddressAdmin)




