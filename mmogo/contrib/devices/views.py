from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from .serializers import DeviceSerializer

from mmogo.contrib.devices.models import Device

class DevicesAPIView(generics.CreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny] # Should be authenticated
    queryset = Device.objects.all()

class DeviceAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [AllowAny] # Should be authenticated
    queryset = Device.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        try:
            device = Device.objects.get(id=kwargs.get('id'))
            device.user = User.objects.get(id=request.data.get('user'))
            device.push_token = request.data.get('push_token')
            device.save()
            serializer = DeviceSerializer(device)

        except Device.DoesNotExist:
            user = request.data.pop('user')
            payload = request.data
            payload[user] = User.objects.get(id=user)
            device = Device.objects.create(**payload)
            serializer = DeviceSerializer(device)

        return Response(serializer.data, status=status.HTTP_200_OK)
