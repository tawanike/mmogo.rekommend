from django.contrib import admin
from .models import SMS

class SMSAdmin(admin.ModelAdmin):
    pass

admin.site.register(SMS, SMSAdmin)

