from django.urls import path

from . import views

urlpatterns = [
    path('/featured', views.FeaturedBrandsAPIView.as_view(), name='featured-brands'),
    path('/<int:brand>/products', views.BrandProductsAPIView.as_view(), name='brand-products'),
    path('/<int:id>', views.BrandAPIView.as_view(), name='brand'),
    path('', views.BrandsAPIView.as_view(), name='brands'),
]
