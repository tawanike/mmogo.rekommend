from django.urls import path
from . import views

urlpatterns = [
    path('/<int:id>', views.StoryAPIView.as_view(), name='story'),
    path('', views.StoriesAPIView.as_view(), name='stories')
]
