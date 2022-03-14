from django.contrib import admin
from .models import Story

class StoryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description',)
    list_display = ('title', 'category', 'published', 'sponsored',)
    list_filter = ('published', 'sponsored',)

admin.site.register(Story, StoryAdmin)