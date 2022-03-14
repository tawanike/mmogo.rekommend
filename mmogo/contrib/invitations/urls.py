from django.urls import path

from . import views

urlpatterns = [
    path('/accept/<str:token>', views.AcceptInviteView.as_view(), name='invite'),
    path('/<str:token>', views.InviteAPIView.as_view(), name='invite'),
    path('', views.InvitesAPIView.as_view(), name='invites'),

]
