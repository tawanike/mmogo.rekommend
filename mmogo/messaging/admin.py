from django.contrib import admin
from .models import Email, SMS


class EmailAdmin(admin.ModelAdmin):
    pass


class SMSAdmin(admin.ModelAdmin):
    pass

admin.site.register(SMS, SMSAdmin)
admin.site.register(Email, EmailAdmin)
