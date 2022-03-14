from django.views import View
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import AllowAny

from mmogo.contrib.invitations.models import Invite
from mmogo.contrib.invitations.serializer import InviteSerializer

class InvitesAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = InviteSerializer
    queryset = Invite.objects.filter()


class InviteAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny,]
    serializer_class = InviteSerializer
    queryset = Invite.objects.filter()
    lookup_field = 'token'


class AcceptInviteView(View):
    template_name = 'pregnancy/accept-invitation.html'

    def get(self, request, token):
        invite = get_object_or_404(Invite, token=token, is_accepted=False)
        if invite:
            invite.is_accepted = True
            invite.token = ''
            invite.save()
        return render(request, self.template_name, context={'invite': invite})
