from django.urls import path


from . import views

urlpatterns = [
    path('/refresh', views.RefreshTokenAPIView.as_view(), name='refresh-token'),
    path('/verify', views.VerifyTokenAPIView.as_view(), name='verify-token'),
    path('', views.GenerateTokenAPIView.as_view(), name='generate-token'),
]
