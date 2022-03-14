from django.contrib import admin
from .models import Brand


class BrandAdmin(admin.ModelAdmin):
    search_fields = ('id', 'title', 'description',)
    list_display = ('title', 'description', 'published',
                    'featured', 'created_at')
    list_filter = ('published', 'featured',)
    prepopulated_fields = {'slug' : ('title',),}


admin.site.register(Brand, BrandAdmin)
