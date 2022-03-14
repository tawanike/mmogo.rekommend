from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from mmogo.contrib.notifications.models import Notification
from mmogo.contrib.notifications.serializers import NotificationSerializer


class NotificationView(APIView):
    def get(self, request, user):
        try:
            notifications = Notification.objects.filter(
                user=user).order_by('-created_at')
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_200_OK)

    def post(self, request, user):
        try:
            notifications = Notification.objects.filter(
                user=user).order_by('-created_at')
            serializer = NotificationSerializer(notifications, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
