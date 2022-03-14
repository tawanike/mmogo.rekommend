from rest_framework import serializers
from django.contrib.auth.models import User

from mmogo.profiles.models import Profile

class ActivateMobileSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, write_only=True)
    user = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        code = data.get('code', None)
        user = data.get('user', None)

        if code is None:
            raise serializers.ValidationError('Code is required.')

        profile = Profile.objects.get(user__id=user, mobile_token=code)
        
        if profile is None:
            raise serializers.ValidationError(
                {'code': 404, 'message': 'Code provided is not valid.'})

        profile.mobile_token = ''
        profile.save()

        user = User.objects.get(id=profile.user.id)
        user.is_active = True
        user.save()

        # TODO: [ZOW-13] Send Welcome Email

        return {
            'status': 'Activated'
        }


class VerifyEmailSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, write_only=True)

    def validate(self, data):
        code = data.get('code')

        if code is None:
            raise serializers.ValidationError('Code is required.')

        profile = Profile.objects.get(token=code)

        if profile is None:
            raise serializers.ValidationError(
                {'code': 404, 'message': 'Code provided is not valid.'})

        if profile.user.is_active:
            profile.token = ''
            profile.save()

        else:
            profile.token = ''
            profile.save()

            user = User.objects.get(id=profile.user.id)
            user.is_active = True
            user.save()

        return {
            'status': 'Activated'
        }