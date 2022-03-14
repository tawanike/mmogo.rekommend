from rest_framework import serializers
from mmogo.profiles.serializers import UserSerializer

from mmogo.contrib.activities.models import Activity

class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Activity
        fields = '__all__'
