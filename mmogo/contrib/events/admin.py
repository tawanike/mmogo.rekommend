from django.contrib import admin
from .models import Event, RSVP

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description',)
    list_display = ('title', 'owner', 'start_date',  'end_date',)
    list_filter = ('published',)    

class RSVPAdmin(admin.ModelAdmin):
    pass

admin.site.register(RSVP, RSVPAdmin)
admin.site.register(Event, EventAdmin)