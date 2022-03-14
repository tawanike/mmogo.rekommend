from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<id>\w+)', views.ActivityAPIView.as_view(), name='activity'),
    url('', views.ActivitiesAPIView.as_view(), name='activities'),
]
