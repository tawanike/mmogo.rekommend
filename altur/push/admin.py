from django.contrib import admin

from altur.push.models import PushNotification, PushToken


class PushNotificationAdmin(admin.ModelAdmin):
    pass

class PushTokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(PushToken, PushTokenAdmin)
admin.site.register(PushNotification, PushNotificationAdmin)