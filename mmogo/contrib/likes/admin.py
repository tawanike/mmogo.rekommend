from django.contrib import admin
from .models import *

class LikeAdmin(admin.ModelAdmin):
    search_fields = ('_id', 'user', 'product',)
    list_display = ('user', 'is_deleted', 'created_at',)
    list_filter = ('is_deleted',)


admin.site.register(Like, LikeAdmin)