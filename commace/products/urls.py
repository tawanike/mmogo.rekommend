from django.urls import path

from . import views

urlpatterns = [
    path('/bundles', views.BundlesAPIView.as_view(),
        name='bundles'),
    path('/bundles/<int:id>', views.BundleAPIView.as_view(),
        name='bundle'),
    path('/bundles/featured', views.FeaturedBundlesAPIView.as_view(),
        name='featured_bundles'),
    path('/featured', views.FeaturedProductAPIView.as_view(),
        name='featured_products'),
    path('/deals', views.DealsAPIView.as_view(),
        name='featured_products'),
    path('/<int:id>', views.ProductAPIView.as_view(), name='product'),

    path(r'title', views.ProductsTitleAPIView.as_view(), name='products_title'),
    path(r'barcode', views.ProductsBarcodeAPIView.as_view(), name='products_barcode'),
    path('', views.ProductsAPIView.as_view(), name='products'),
]
