from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'countries/(?P<country>\w+)/provinces', views.CountryProvincesAPIView.as_view(), name='country_provinces'),
    url(r'provinces/(?P<province>\w+)/cities', views.ProvinceCitiesAPIView.as_view(), name='country_provinces'),
    url(r'provinces', views.ProvinceView.as_view(), name='index'),
    url(r'countries', views.CountriesAPIView.as_view(), name='countries'),
    url(r'cities', views.CitiesAPIView.as_view(), name='cities'),
]
