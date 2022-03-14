from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<user>\w+)/(?P<object_type>\w+)/(?P<object_id>\w+)',
        views.RatingsAPIView.as_view(), name='ratings'),
    url('', views.RateAPIView.as_view(), name='rate'),
]
