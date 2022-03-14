from rest_framework import serializers
from .models import Event, RSVP

from mmogo.profiles.serializers import UserSerializer
from mmogo.contrib.medialibrary.serializers import MediaLibrarySerializer


class EventSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    attachments = MediaLibrarySerializer(read_only=True, many=True)

    class Meta:
        model = Event
        fields = '__all__'

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = '__all__'