from .models import Order, OrderStatus
from .serializers import OrderSerializer, OrderStatusSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class OrdersAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'tracking_code'

class OrderAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_field = 'id'
    
class OrderStatusAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = OrderStatusSerializer

    def get_queryset(self):
        queryset = OrderStatus.objects.filter(order__id=self.kwargs.get('id')).order_by('status')
        return queryset
