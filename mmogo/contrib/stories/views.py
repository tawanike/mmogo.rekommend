from rest_framework.permissions import AllowAny
from rest_framework import generics

from mmogo.contrib.stories.models import Story
from mmogo.contrib.stories.serializer import StorySerializer

class StoriesAPIView(generics.ListAPIView):
    serializer_class = StorySerializer
    permission_classes = [AllowAny]
    queryset = Story.objects.filter(published=True).order_by('ordering')


class StoryAPIView(generics.RetrieveAPIView):
    serializer_class = StorySerializer
    permission_classes = [AllowAny]
    queryset = Story.objects.filter(published=True).order_by('ordering')
    lookup_field = 'id'
