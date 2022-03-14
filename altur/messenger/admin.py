from django.contrib import admin
from .models import Messenger


class MessengerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Messenger, MessengerAdmin)
