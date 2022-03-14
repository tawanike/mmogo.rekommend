from django.urls import path
from . import views
    
    
urlpatterns = [
   
    path('/featured', views.FeaturedCategories.as_view(), name='featured_categories'),
    path('/parent', views.ParentCategories.as_view(), name='parent_categories'),
    path('/subcategories/<int:id>/products', views.SubCategoryCategoryProducts.as_view(), name='subcategory_products'),
    path('/<int:id>', views.CategoryAPIView.as_view(), name='category'),
    # path('/<int:id>/featured', views.FeaturedCategoryProductsAPIView.as_view(), name='featured-category-products'),
    path('/<int:id>/subcategories', views.SubcategoryAPIView.as_view(), name='subcategories'),
    path('/<int:id>/products', views.CategoryProductsAPIView.as_view(), name='category-products'),

    path('',  views.CategoriesAPIView.as_view(), name='all_categories'),
]