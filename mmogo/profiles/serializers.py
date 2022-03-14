import uuid
import random
import string

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.template import Context, Engine
from django.contrib.auth.models import User, Group

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from sentry_sdk import capture_exception

from mmogo.profiles.models import Profile
from mmogo.contrib.locations.models import Country
from mmogo.contrib.locations.serializers import CountrySerializer

from altur.email.models import Email
# from altur.sms.models import SMS
from altur.sms.utils import generate_mobile_code

class UserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(source='user_profile.mobile', read_only=True)
    image = serializers.ImageField(source='user_profile.image', read_only=True)
    cover = serializers.ImageField(source='user_profile.cover', read_only=True)
    invitation_code = serializers.CharField(source='user_profile.invitation_code', read_only=True)
    is_guest = serializers.BooleanField(source='user_profile.is_guest', read_only=True)
    onboarded = serializers.BooleanField(source='user_profile.onboarded', read_only=True)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                group = Group.objects.get(name='Users')
                password = validated_data['password']
                validated_data.pop('password')

                token = str(uuid.uuid4())
                email = validated_data['email']
                mobile_token = generate_mobile_code()
                invitation_code = ''.join(random.choice(string.ascii_letters) for x in range(7))

                try:
                    user = User.objects.get(email=email)
                    if user:
                        key_error = "user_exists"
                        raise ValidationError('Email address taken.', code=key_error)
                except User.DoesNotExist:
                    user = User.objects.create(**validated_data)
                    user.username = email
                    user.set_password(password)
                    user.groups.add(group)
                    user.save()

                    profile = Profile.objects.create(
                        user=user,
                        token=token,
                        country=Country.objects.get(slug='south-africa'),
                        mobile_token=mobile_token,
                        invitation_code=invitation_code
                    )

                    # Send email notification
                    engine = Engine.get_default()
                    context = Context({
                        "first_name": validated_data['first_name'],
                        "token": token,
                        'mobile_token': mobile_token,
                    })
                    
                    context = Context(context)
                    template = engine.get_template('email/activation.html')
                    body = template.render(context)

                    Email.objects.create(
                        subject='ZowZow Account Activation',
                        from_address=settings.POSTMAN,
                        body=body,
                        recipient=validated_data['email'],
                        service='SES',
                    )

                    # Notify Slack

                    if settings.REQUIRE_MOBILE:
                        mobile = validated_data['mobile']
                        profile.mobile = mobile
                        profile.save()

                        sms_context = Context({
                            "code": mobile_token
                        })
                        template = engine.get_template('sms/activation.txt')
                        sms_body = template.render(sms_context)

                        # SMS.objects.create(
                        #     from_number=settings.TWILIO_FROM_NUMBER,
                        #     recipient=format_mobile(mobile),
                        #     body=sms_body,
                        #     service='TWILIO'
                        # )

                return user
        except Exception as error:
            print('PANO', error) # TODO Handle errors appropriately and use HTTP error codes
            capture_exception(error)
            return {"message": str(error)}

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'last_name', 'password', 'email', 'mobile', 'is_active',
            'image', 'cover', 'mobile', 'invitation_code', 'is_guest', 'onboarded'
        ]
        extra_kwargs = {'password': {'write_only': True}, 'mobile': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = "__all__"

class ForgotPasswordSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, data):
        user = get_object_or_404(User, email=data['email'])
        token = default_token_generator.make_token(user)
        mobile_token = generate_mobile_code()

        profile = Profile.objects.get(user=user)
        profile.token = token
        profile.mobile_token = mobile_token
        profile.save()

        engine = Engine.get_default()
        context = Context({
            "user": user,
            "mobile_token": mobile_token
        })
                
        template = engine.get_template('email/password_reset.html')
        context = Context(context)
        body = template.render(context)

        Email.objects.create(
            subject='Password Reset on ZowZow',
            from_address=settings.POSTMAN,
            body=body,
            recipient=data['email'],
            service='SES',
        )
        message = 'Reset Instructions has been sent to your email'
        return {'code': 200, 'message': message}

class CreatePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True)
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    message = serializers.CharField(read_only=True)

    default_error_messages = {
        "invalid_token": "Invalid token for given user.",
        "invalid_uid": "Invalid user id or user doesn't exist.",
    }

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password = validated_data['password']
        code = validated_data['code']

        try:
            profile = Profile.objects.get(mobile_token=code)
        except (Profile.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"code": self.error_messages[key_error]}, code=key_error
            )

        if profile:
            user = User.objects.get(pk=profile.user.id)
            message = 'Password Change Successful'
            user.set_password(password)
            user.is_active = True
            user.save()

            profile.mobile_token = ''
            profile.save()

            engine = Engine.get_default()
            context = Context({
                "user": user 
            })
                    
            template = engine.get_template('email/password_changed_confirmation.html')
            context = Context(context)
            body = template.render(context)

            Email.objects.create(
                subject='ZowZow Baby password has been changed!',
                from_address=settings.POSTMAN,
                body=body,
                recipient=user.email,
                service='SES',
            )

            return {'message': message}
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": self.error_messages[key_error]}, code=key_error
            )
    
class ChangePasswordSerializer(serializers.Serializer):
    message = serializers.CharField(read_only=True)
    user = serializers.IntegerField(write_only=True)
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    default_error_messages = {
        "invalid_password": "Invalid Password for user",
        "password_mismatch": "Passwords do not match",
    }


    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password = validated_data['password']
        new_password = validated_data['new_password']
        confirm_password = validated_data['confirm_password']
        mobile_token = generate_mobile_code()

        profile = Profile.objects.get(user__id=validated_data['user'])
        profile.token = token = default_token_generator.make_token(profile.user)
        profile.mobile_token = mobile_token
        profile.save()

        engine = Engine.get_default()
        context = Context({
            "user": profile.user,
            "token": token
        })
                
        template = engine.get_template('email/password_changed_confirmation.html')
        context = Context(context)
        body = template.render(context)

        Email.objects.create(
            subject='ZowZow Baby password has been changed!',
            from_address=settings.POSTMAN,
            body=body,
            recipient=profile.user.email,
            service='SES',
        )


        get_user = self.context['request'].user
        user = get_object_or_404(User, email=get_user)
        password_correct = check_password(password, user.password)

        if password_correct:
            if new_password == confirm_password:
                message = 'Password Changed Successfully'
                user.set_password(new_password)
                user.save()
                return {'message': message}
            else:
                key_error = 'password_mismatch'
                raise ValidationError(
                     {'password_mismatch': self.error_messages[key_error]}, code=key_error
                )
        else:
            key_error = 'invalid_password'
            raise ValidationError(
                {'password': self.error_messages[key_error]}, code=key_error
            )

    def create(self, validated_data):
        print(validated_data)
        

        return {'message': 'Password changed'}

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
