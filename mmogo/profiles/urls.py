from django.urls import path

from . import views

from commace.contrib.cart.views import UserCartAPIView
from commace.contrib.shoppinglists.views import UserShoppinglistsAPIView

from mmogo.contrib.addresses.views import UserAddressesAPIView
from mmogo.contrib.events.views import UserEventsAPIView

urlpatterns = [
    path('/me', views.UserAPIView.as_view(), name='user'),
    path('/forgot-password', views.ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('/change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('/create-password', views.CreatePasswordAPIView.as_view(), name='create-password'),

    path('/<int:user>/addresses', UserAddressesAPIView.as_view(), name='addresses'),
    path('/<int:user>/carts', UserCartAPIView.as_view(), name='caregivers'),
    path('/<int:user>/registries', UserShoppinglistsAPIView.as_view(), name='user_registry'),
    path('/<int:user>/events', UserEventsAPIView.as_view(), name='userevents'),
    path('/<int:id>', views.ProfileAPIView.as_view(), name='user-profile'),
    path('', views.UsersAPIView.as_view(), name='users'),
]
