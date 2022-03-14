from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from commace.contrib.promocodes.models import PromoCode, Redemption
from commace.contrib.promocodes.serializer import PromoCodeSerializer, RedemptionSerializer

class PromoCodeAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = PromoCodeSerializer
    queryset = PromoCode.objects.filter(published=True, is_active=True)

class RedemptionAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = RedemptionSerializer
    