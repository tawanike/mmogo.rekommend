from rest_framework import serializers

from .models import MediaLibrary


class MediaLibrarySerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaLibrary
        fields = "__all__"

class AltMediaLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaLibrary
        fields = ('id', 'title', 'description', 'file', 'file_type', 'is_enhanced',)