from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url(r'push', views.PushNotificationsView.as_view()),
    url(r'push/sends', csrf_exempt(views.PushNotifyView.as_view())),
    # url('^(?P<user>[a-zA-Z0-9-]+)$', views.NotificationView.as_view(), name='notifications'),
]
