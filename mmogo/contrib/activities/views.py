from rest_framework import generics
from mmogo.contrib.activities.models import Activity
from mmogo.contrib.activities.serializers import ActivitySerializer

class ActivitiesAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()

class ActivityAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.all()
