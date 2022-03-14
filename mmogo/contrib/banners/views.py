from rest_framework.generics import ListAPIView
from .serializers import BannerSerializer
from .models import Banner
from rest_framework.permissions import AllowAny

# Create your views here.
class BannersAPIView(ListAPIView):
    permission_classes = [AllowAny,]
    serializer_class = BannerSerializer
    queryset = Banner.objects.filter(published=True)