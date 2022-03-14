from django.urls import path


from . import views

urlpatterns = [
    path('/email', views.VerifyEmailAPIView.as_view(), name='verify-email'),
    path('/mobile', views.ActivateMobileAPIView.as_view(), name='activate-mobile'),
]
