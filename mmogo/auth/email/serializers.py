from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from mmogo.profiles.models import Profile
from mmogo.profiles.serializers import UserSerializer

class EmailLogInSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(max_length=255, read_only=True)
    last_name = serializers.CharField(max_length=255, read_only=True)
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    is_active = serializers.BooleanField(read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    mobile = serializers.CharField(source='user_profile.mobile', read_only=True)
    image = serializers.ImageField(source='user_profile.image', read_only=True)
    cover = serializers.ImageField(source='user_profile.cover', read_only=True)
    invitation_code = serializers.CharField(source='user_profile.invitation_code', read_only=True)
    is_guest = serializers.ImageField(source='user_profile.is_guest', read_only=True)
    onboarded = serializers.ImageField(source='user_profile.onboarded', read_only=True)

    def to_representation(self, instance):
        representation = super(EmailLogInSerializer, self).to_representation(instance)
        profile = Profile.objects.get(user__id=instance.get('id'))
        representation['invitation_code'] = profile.invitation_code
        representation['is_guest'] = profile.is_guest
        representation['mobile'] = profile.mobile
        if profile.image:
            representation['image'] = profile.image
        if profile.cover:
            representation['cover'] = profile.cover
        representation['onboarded'] = profile.onboarded
        return representation

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError('Email is required.')

        if password is None:
            raise serializers.ValidationError('Password is required.')

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError('Email/Password provided is not valid.')

        if not user.is_active:
            raise serializers.ValidationError({'code': 403, 'message': 'Account is not activated.', 'user': user.id })

        profile = Profile.objects.get(user=user)
        refresh = RefreshToken.for_user(user)

        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_active': user.is_active,
            'image': profile.image,
            'mobile': profile.mobile,
            'cover': profile.cover,
            'invitation_code': profile.invitation_code,
            'token': token,
            'is_guest': profile.is_guest,
            'onboarded': profile.onboarded,
        }


# Email activation/confirmation