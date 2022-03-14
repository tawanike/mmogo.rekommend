from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<objectId>\w+)/(?P<objectType>\w+)', views.UploadsAPIView.as_view(), name='images'),
    url('', views.ImageView.as_view(), name='image'),
]
