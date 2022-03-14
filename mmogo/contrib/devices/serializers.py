import uuid

from rest_framework import serializers

from mmogo.contrib.devices.models import Device

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ['device_id']

    def create(self, validated_data):
        device = Device()
        device.app_version = validated_data['app_version']
        device.device_id = str(uuid.uuid4())
        device.online = True
        
        device.device_name = validated_data['device_name']
        device.device_year_class = validated_data['device_year_class']
        device.device_expo_version = validated_data['device_expo_version']
        device.platform = str(validated_data['platform'])
        device.native_app_version = validated_data['native_app_version']
        device.native_build_version = validated_data['native_build_version']

        device.save()
        return device

    def update(self, instance, validated_data):
        try:
            device = Device.objects.get(id=instance.id)
            return device
            
        except Device.DoesNotExist:
            device = Device()
            device.app_version = validated_data['app_version']
            device.device_id = str(uuid.uuid4())
            device.online = True
            
            device.device_name = validated_data['device_name']
            device.device_year_class = validated_data['device_year_class']
            device.device_expo_version = validated_data['device_expo_version']
            device.platform = str(validated_data['platform'])
            device.native_app_version = validated_data['native_app_version']
            device.native_build_version = validated_data['native_build_version']

            device.save()
            return device

        