import uuid
from django.conf import settings
from django.template import Context, Engine, Context

from rest_framework import serializers

from altur.email.models import Email

from mmogo.contrib.invitations.models import Invite


class InviteSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)

    def create(self, validated_data):
        token = str(uuid.uuid4())
        invite = super().create(validated_data)
        invite.token = token
        invite.save()

         # Send email notification
        engine = Engine.get_default()
        context = Context({
            "first_name": validated_data['first_name'],
            "token": token,
            "invitee": invite.user
        })
        
        template = engine.get_template('pregnancy/pregnancy-invitation.html')
        context = Context(context)
        body = template.render(context)


        Email.objects.create(
            subject='ZowZow Baby Invitation',
            from_address=settings.POSTMAN,
            body=body,
            recipient=validated_data['email'],
            service='SENDGRID',
        )

        return invite

    class Meta:
        model = Invite
        fields = '__all__'
