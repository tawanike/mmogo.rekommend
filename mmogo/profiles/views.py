import uuid
from django.conf import settings
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.template import Context, Engine

from mmogo.profiles.serializers import (
    ChangePasswordSerializer, CreatePasswordSerializer, ForgotPasswordSerializer, 
    UserSerializer
)
from mmogo.profiles.models import Profile
from mmogo.auth.email.serializers import EmailLogInSerializer

from altur.sms.models import SMS
from altur.email.models import Email
from altur.sms.utils import generate_mobile_code, format_mobile



class UsersAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny,]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 


class CreatePasswordAPIView(APIView):
    serializer_class = CreatePasswordSerializer
    permission_classes = [AllowAny,]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK) 

class ChangePasswordView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()

    # def post(self, request):
    #     print(request.data)
    #     serializer = self.serializer_class(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         print(serializer.data)
    #     else:
    #         print(serializer.errors)
    #     return Response(serializer.data, status=status.HTTP_200_OK) 

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    # serializer_class = UserSerializer
    
    def put(self, request, id):
        data = request.data
        user = User.objects.get(id=id)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
 
        if data.get('email') != user.email:
            user.email = data.get('email', user.email)
            user.username = data.get('email', user.email)
        user.save()

        token = str(uuid.uuid4())
        engine = Engine.get_default()
        context = Context({
            "first_name": user.first_name,
            "token": token
        })
        
        context = Context(context)
        template = engine.get_template('email/email_reset.html')
        body = template.render(context)

        Email.objects.create(
            subject='ZowZow Baby | Confirm Email Address',
            from_address=settings.POSTMAN,
            body=body,
            recipient=user.email,
            service='SES',
        )

        instance = Profile.objects.get(user__id=id)
        instance.is_guest = data.get('is_guest', instance.is_guest)
        instance.onboarded = data.get('onboarded', instance.onboarded)

        # If mobile number changes
        if data.get('mobile') != instance.mobile:
            code = generate_mobile_code()
            instance.mobile_token = code
            instance.mobile = format_mobile(data.get('mobile', instance.mobile))

            SMS.objects.create(
                recipient = format_mobile(data.get('mobile')),
                body = f"Your ZowZow Baby code is {code}. Never share this code.",
                service= settings.SMS_SERVICE,
                from_number='ZowZow'
            )

        instance.image = data.get('image', instance.image)
        instance.cover = data.get('cover', instance.cover)
        instance.save()

        return Response(EmailLogInSerializer({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile': instance.mobile,
            'is_active': user.is_active,
            'is_guest': instance.is_guest,
            'onboarded': instance.onboarded,
            'image': instance.image,
            'cover': instance.cover,
            'invitation_code': instance.invitation_code,
            'verified': False
        }).data, status=status.HTTP_200_OK) 