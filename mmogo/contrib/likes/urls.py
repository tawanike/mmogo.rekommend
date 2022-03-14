from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<user>\w+)', views.LikesAPIView.as_view(), name='likes'),
    # url(r'(?P<id>\w+)', views.UnLikeAPIView.as_view(), name='unlike'),
    url('', views.LikeAPIView.as_view(), name='like'),

]
