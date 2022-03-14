from django.contrib import admin
from .models import Tracker


class TrackerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tracker, TrackerAdmin)
