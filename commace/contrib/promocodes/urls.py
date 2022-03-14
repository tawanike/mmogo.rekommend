from django.conf.urls import url

from . import views

urlpatterns = [
    url('', views.RedemptionAPIView.as_view(), name='like'),
]
