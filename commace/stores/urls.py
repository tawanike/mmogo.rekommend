from django.urls import path

from . import views

urlpatterns = [
    path('/<int:id>/categories/<int:category>', views.StoreCategoryProducts.as_view(), name='shop_categories'),
    path('/<int:id>/categories', views.StoreCategories.as_view(), name='shop_categories'),
    path('/<int:shop>/products', views.StoreProducts.as_view(), name='shop_products'),
    path('/featured', views.FeaturedStoresAPIView.as_view(), name='featured-stores'),
    path('/<int:id>', views.StoreAPIView.as_view(), name='shop'),
    path('', views.StoresAPIView.as_view(), name='shops'),
]
