from django.contrib import admin
from .models import Store


class StoreAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'title', 'slug', 'cover', 'description', 'image',)
    list_display = ('title', 'description', 'ordering',
                    'featured', 'published', 'created_at',)
    list_filter = ('featured', 'published',)
    prepopulated_fields = {'slug' : ('title',),}


admin.site.register(Store, StoreAdmin)
