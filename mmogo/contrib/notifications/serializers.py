from rest_framework import serializers
from mmogo.contrib.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('id', 'title', 'subtitle', 'description', 'user', 'created_at', 'updated_at', 'sender')

