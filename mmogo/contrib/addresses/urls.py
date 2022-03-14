from django.urls import path

from . import views

urlpatterns = [
    path('/<int:id>', views.AddressAPIView.as_view(), name='address'),
    path('', views.AddressesAPIView.as_view(), name='addresses'),
]
