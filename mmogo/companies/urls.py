from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'(?P<company>[a-zA-Z0-9-]+)/requests',
        views.CompanyRequest.as_view(), name='company_requests'),
    url(r'(?P<company>\w+)/users',
        views.CompanyLocationsAPIView.as_view(), name='company_users'),
    url(r'(?P<company>\w+)/locations',
        views.CompanyLocationsAPIView.as_view(), name='company_locations'),
    url(r'(?P<company>\w+)/suppliers',
        views.CompanySuppliersAPIView.as_view(), name='company_suppliers'),
    url(r'(?P<company>[a-zA-Z0-9-]+)',
        views.CompanyAPIView.as_view(), name='company'),
    url('', views.CompaniesAPIView.as_view(), name='companies'),


]
