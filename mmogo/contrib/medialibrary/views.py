from rest_framework import generics

from mmogo.utils import upload
from mmogo.contrib.medialibrary.models import MediaLibrary
from mmogo.contrib.medialibrary.serializers import MediaLibrarySerializer


class MediaLibraryAPIView(generics.ListAPIView):
    serializer_class = MediaLibrarySerializer
    queryset = MediaLibrary.objects.filter(published=True)
