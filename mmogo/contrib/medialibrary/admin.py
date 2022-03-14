from django.contrib import admin
from .models import MediaLibrary


class MediaLibraryAdmin(admin.ModelAdmin):
    search_fields = ('id', 'file', 'title',
                     'file_type', 'description',)
    list_display = ('title', 'file_type', 'description',
                    'published', 'featured', 'is_enhanced', 'created_at',)
    list_filter = ('published', 'featured', 'is_enhanced',)
    prepopulated_fields = {'slug' : ('title',),}


admin.site.register(MediaLibrary, MediaLibraryAdmin)
