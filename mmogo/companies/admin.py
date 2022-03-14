from django.contrib import admin
from .models import *

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'phone', 'email', 'website', 'phone', 'description', )
    list_display = ('title', 'description',  'email', 'website', 'phone',)

admin.site.register(Company, CompanyAdmin)