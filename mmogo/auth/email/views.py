from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import EmailLogInSerializer
from mmogo.auth.renders import UserJSONRenderer


class SignInAPIView(APIView):
    # renderer_class = UserJSONRenderer
    serializer_class = EmailLogInSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            print(data)
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(error)
            return Response({'message': str(error) }, status=status.HTTP_400_BAD_REQUEST)
