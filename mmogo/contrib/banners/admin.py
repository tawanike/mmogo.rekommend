from django.contrib import admin
from .models import Banner

# Register your models here.
class BannerAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description',)
    list_display = ('title', 'description','published',  'featured',)
    list_filter = ('published', 'featured',)    
    prepopulated_fields = {'slug' : ('title',),}

admin.site.register(Banner, BannerAdmin)
