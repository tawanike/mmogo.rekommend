from django.urls import path
from . import views

urlpatterns = [
    # path('/webhook', views.WebhookAPIView.as_view(), name='webhook'),
    # path('/customer', views.CustomerAPIView.as_view(), name='customer'),
    # path('/<int:payment_id>', views.PaystackPaymentAPIView.as_view(), name='payment'),
    path('', views.PaystackPaymentsAPIView.as_view(), name='payments'),
]
