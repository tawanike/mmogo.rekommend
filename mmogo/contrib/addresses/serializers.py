from mmogo.contrib.addresses.models import Address
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().update(instance, validated_data)
        
    class Meta:
        model = Address
        fields = '__all__'
        read_only_fields = ['user', ]


