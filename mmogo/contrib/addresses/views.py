from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from mmogo.contrib.addresses.models import Address
from mmogo.contrib.addresses.serializers import AddressSerializer

class AddressesAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

class AddressAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    lookup_field = 'id'

class UserAddressesAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = AddressSerializer
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)