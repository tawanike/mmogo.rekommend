from . import views
from django.urls import path

urlpatterns = [
    path('/reservations', views.ProductReservedAPIView.as_view(), name='product-reservation'),
    path('/reservations/<int:user>', views.ProductReservedAPIView.as_view(), name='product-reservations'),
    path('/invitations', views.ShoppingListContributorsView.as_view(), name='shoppinglistcontributor-invite'),
    path('/invitations/<str:token>', views.ShoppingListContributorView.as_view(), name='shoppinglistcontributor-detail'),
    path('/<int:shoppinglist>/products', views.ShoppingListItemsAPIView.as_view(), name='shoppinglistitems'),
    path('/<int:shoppinglist>/products/<int:product>', views.ShoppingListItemView.as_view(), name='shoppinglistitem-detail'),
    path('/featured', views.FeaturedShoppingListView.as_view(),name='featured-shoppinglist'),
    path('/<int:id>', views.ShoppingListView.as_view(), name='shoppinglist-detail'),
    path('', views.ShoppingListsView.as_view(), name='shoppinglist'),
]
