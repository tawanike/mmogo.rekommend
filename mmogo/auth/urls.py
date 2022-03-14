from django.urls import path, include


urlpatterns = [
    path('/email', include('mmogo.auth.email.urls')),
    path('/token', include('mmogo.auth.token.urls')),
    path('/activate', include('mmogo.auth.activate.urls')),
]
