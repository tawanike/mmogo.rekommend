from django.urls import path
from .views import OrdersAPIView, OrderDetailView, OrderAPIView, OrderStatusAPIView

urlpatterns = [
    path('/detail/<str:tracking_code>', OrderDetailView.as_view(), name='order-detail'),
    path('/<int:id>/tracking', OrderStatusAPIView.as_view(), name='order-status'),
    path('/<int:id>', OrderAPIView.as_view(), name='order-detail'),
    path('', OrdersAPIView.as_view(), name='orders')
]
