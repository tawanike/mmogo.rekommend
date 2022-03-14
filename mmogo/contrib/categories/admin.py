from django.contrib import admin
from .models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'slug',)
    list_display = ('title', 'published', 'featured', 'is_parent',)
    list_filter = ('published', 'featured','is_parent',)
    prepopulated_fields = {'slug' : ('title',),}

admin.site.register(Category, CategoryAdmin)