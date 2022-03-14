from django.contrib import admin
from .models import Link

class LinkAdmin(admin.ModelAdmin):
    search_fields = ('id', 'link',)
    list_display = ('type_display', 'link',)



admin.site.register(Link, LinkAdmin)