from django.urls import path
from . import views

from commace.contrib.promocodes.views import  RedemptionAPIView

urlpatterns = [
    path('/<int:id>/promocodes', RedemptionAPIView.as_view()),
    path('/<int:id>/products', views.CartItemAPIView.as_view()),
    path('/<int:id>', views.CartAPIView.as_view()),
    path('', views.CartsAPIView.as_view()),
]
