import requests, json, os
from sentry_sdk import capture_exception

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import PaystackSerializer

from commace.payments.models import Payment

class PaystackPaymentsAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaystackSerializer
    queryset = Payment.objects.all()

class PaystackPaymentAPIView(generics.CreateAPIView):
    # permission_classes = [AllowAny,]
    serializer_class = PaystackSerializer
    lookup_field = 'payment_id'


import pprint, os
class WebhookAPIView(generics.CreateAPIView):
    def post(self, request):
        pprint.pprint(request.data)

        return Response({'code': 200, 'message': ''}, status=status.HTTP_200_OK)

class CustomerAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        sec_key = os.environ.get("PAYSTACK_SECRET_KEY")

        url = 'https://api.paystack.co/customer'
        try:
            data = request.data
            headers = {'Authorization': 'Bearer ' + sec_key, 'Content-Type': 'application/json'}
            request = requests.post(url=url, headers=headers, data=json.dumps(data))
            response = request.json()
            message = response['message']
            return Response({'code': 200, 'message': message}, 
                                status=status.HTTP_200_OK)
        except Exception as error:
            capture_exception(error)
            return Response({'code': 400, 'message': str(error)}, 
                                status=status.HTTP_400_BAD_REQUEST) 