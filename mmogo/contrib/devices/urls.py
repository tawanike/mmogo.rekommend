from django.urls import path


from . import views

urlpatterns = [
    path('/registrations', views.DevicesAPIView.as_view(), name='device-register'),
    path('/<int:id>', views.DeviceAPIView.as_view(), name='update-device'),
]
