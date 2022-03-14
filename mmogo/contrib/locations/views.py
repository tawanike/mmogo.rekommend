import json
from slugify import slugify
from rest_framework import status
from bson.objectid import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from mmogo.contrib.locations.models import Province, Country, City
from mmogo.contrib.locations.serializers import ProvinceSerializer

class ProvinceView(APIView):
    def get(self, request):
        try:
            response = []
            provinces = Province.objects.all()
            for province in provinces:
                response.append({
                    'id': str(province.id),
                    'title': province.title,
                    'subtitle': province.subtitle,
                    'slug': province.slug,
                    'code': {
                        'id': str(province.country.id),
                        'title': province.country.title,
                        'subtitle': province.country.subtitle,
                        'slug': province.country.slug,
                        'code': province.country.code,
                    }
                })

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'code': 500,
                'message': str(e),
            })
    
    def post(self, request):
        try:
            province = Province()
            province.title = request.data.get('title')
            province.slug = slugify(request.data.get('title'))
            province.country = Country.objects.get(_id=ObjectId(request.data.get('country')))
            province.save()

            return Response({
                    'id': str(province.id),
                    'title': province.title,
                    'subtitle': province.subtitle,
                    'slug': province.slug,
                    'country': str(province.country),
                }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'code': 500,'message': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CitiesAPIView(APIView):
    def get(self, request):
        try:
            response = []
            cities = City.objects.all()
            for city in cities:
                response.append({
                    'id': str(city.id),
                    'title': city.title,
                    'subtitle': city.subtitle,
                    'slug': city.slug,
                    'province': {
                        'id': str(city.province.id),
                        'title': city.province.title,
                        'subtitle': city.province.subtitle,
                        'slug': city.province.slug,
                        'country': city.province.country.title,
                    }
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'code': 500,
                'message': str(e),
            })

    def post(self, request):
        try:
            city = City()
            city.title = request.data.get('title')
            city.slug = slugify(request.data.get('title'))
            city.province = Province.objects.get(_id=ObjectId(request.data.get('province')))
            city.save()

            return Response({
                    'id': str(city.id),
                    'title': city.title,
                    'subtitle': city.subtitle,
                    'slug': city.slug,
                    'province': str(city.province)
                }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'code': 500,'message': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountriesAPIView(APIView):
    def get(self, request):
        try:
            response = []
            countries = Country.objects.all()
            for country in countries:
                response.append({
                    'id': str(country.id),
                    'title': country.title,
                    'subtitle': country.subtitle,
                    'slug': country.slug,
                    'code': country.code,
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'code': 500,'message': str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            country = Country()
            country.title = request.data.get('title')
            country.slug = slugify(request.data.get('title'))
            country.code = request.data.get('code').lower()
            country.save()
            return Response({
                    'id': str(country.id),
                    'title': country.title,
                    'subtitle': country.subtitle,
                    'slug': country.slug,
                    'code': country.code,
                }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'code': 500,'message': str(error) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CountryProvincesAPIView(APIView):
    def get(self, request, country):
        try:
            response = []
            provinces = Province.objects.filter(country=country)
            for province in provinces:
                response.append({
                    'id': str(province.id),
                    'title': province.title,
                    'subtitle': province.subtitle,
                    'slug': province.slug,
                    'code': {
                        'id': str(province.country),
                        'title': province.country.title,
                        'subtitle': province.country.subtitle,
                        'slug': province.country.slug,
                        'code': province.country.code,
                    }
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'code': 500,
                'message': str(e),
            })

class ProvinceCitiesAPIView(APIView):
    def get(self, request, province):
        try:
            response = []
            cities = City.objects.filter(province=province)
            for city in cities:
                response.append({
                    'id': str(city.id),
                    'title': city.title,
                    'subtitle': city.subtitle,
                    'slug': city.slug,
                    'code': {
                        'id': str(city.province.id),
                        'title': city.province.title,
                        'subtitle': city.province.subtitle,
                        'slug': city.province.slug,
                        'country': city.province.country.title,
                    }
                })
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'code': 500,
                'message': str(e),
            })

