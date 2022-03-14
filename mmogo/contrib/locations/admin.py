from django.contrib import admin
from .models import *

class CountryAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'title', 'description', 'currency', 'subtitle', 'code',)
    list_display = ('title', 'code', 'currency',)


class CityAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'title', 'description',  'subtitle', 'country',)
    list_display = ('title', 'subtitle', 'description',)


class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'title', 'description',  'subtitle', 'province',)
    list_display = ('title', 'subtitle', 'description',)
 


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Province, ProvinceAdmin)