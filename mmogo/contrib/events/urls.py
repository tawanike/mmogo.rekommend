from django.urls import path
from . import views

urlpatterns = [
    path('/<int:id>/rsvp', views.RSVPAPIView.as_view(), name='rsvp'),
    path('/<int:id>', views.EventAPIView.as_view(), name='event'),
    path('', views.EventsAPIView.as_view(), name='events')
]
