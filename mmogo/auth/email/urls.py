from django.urls import path


from . import views

urlpatterns = [
    path('', views.SignInAPIView.as_view(), name='email-signin'),
]
