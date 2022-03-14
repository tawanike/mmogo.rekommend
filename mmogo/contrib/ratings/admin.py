from django.contrib import admin
from .models import *

class RatingAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'object_id', 'user', 'rating', 'object_type',)
    list_display = ('user', 'object_id', 'rating', 'object_type', 'created_at',)
    list_filter = ('is_deleted',)

admin.site.register(Rating, RatingAdmin)