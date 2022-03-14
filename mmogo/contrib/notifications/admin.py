from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description', 'status', 'sender', 'user',)
    list_display = ('title', 'description', 'status', 'sender', 'user',)
    list_filter = ('status',)

admin.site.register(Notification, NotificationAdmin)
