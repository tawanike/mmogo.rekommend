from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ('mobile',)
    list_filter = ('first_login', )


admin.site.register(Profile, ProfileAdmin)
