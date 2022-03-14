from django.contrib import admin
from .models import Invite

class InviteAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'email', 'token', 'last_name')
    list_display = ('first_name', 'last_name', 'is_accepted', 'created_at',)
    list_filter = ('is_accepted',)

admin.site.register(Invite, InviteAdmin)