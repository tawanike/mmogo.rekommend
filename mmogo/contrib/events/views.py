from django.db.models import Prefetch
from django.db.models import Q

from rest_framework import generics

from .serializers import EventSerializer, RSVPSerializer
from .models import Event, RSVP
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class EventsAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = EventSerializer
    queryset = Event.objects.prefetch_related(Prefetch('users'), Prefetch('attachments')).select_related('owner').all()

class EventAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = EventSerializer
    queryset = Event.objects.prefetch_related(Prefetch('users'), Prefetch('attachments')).select_related('owner').all()

class RSVPAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = RSVPSerializer
    queryset = RSVP.objects.select_related('calendar', 'user').all()

class UserEventsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = EventSerializer
    queryset = Event.objects.prefetch_related(
        Prefetch('users'), Prefetch('attachments')).select_related('owner').all()
    
    def get_queryset(self):
        user = self.request.user.id
        queryset = Event.objects.prefetch_related(
            Prefetch('users'), Prefetch('attachments')
        ).select_related('owner').filter(Q(owner=user) | Q(users__in=[user]))

        return queryset