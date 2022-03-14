from django.urls import path, include

urlpatterns = [
    path('/paystack', include('commace.payments.paystack.urls'))
]
