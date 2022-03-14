from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from mmogo.auth.renders import UserJSONRenderer
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            refresh = RefreshToken(request.data.get('refresh'))
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(token, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response({'error': str(error) }, status=status.HTTP_400_BAD_REQUEST)


class GenerateTokenAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            print(error)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
