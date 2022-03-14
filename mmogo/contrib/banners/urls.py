from django.urls import path
from . import views

urlpatterns = [
    path('', views.BannersAPIView.as_view(), name='banners')
]
