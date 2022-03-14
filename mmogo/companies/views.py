from slugify import slugify
from datetime import datetime
from rest_framework import status
from bson.objectid import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from sentry_sdk import capture_exception

from commace.companies.models import Company
from commace.contrib.requests.models import Request
from commace.contrib.warehouses.models import Warehouse
from commace.contrib.suppliers.models import Supplier, CompanySupplier
from commace.contrib.warehouses.serializer import warehouse_serializer
from commace.contrib.requests.serializer import order_request_serializer
from commace.contrib.suppliers.serializer import company_supplier_serializer


class CompaniesAPIView(APIView):
    def get(self, request):
        try:
            response = []
            shops = Company.objects.all()
            for shop in shops:
                response.append({
                    'id': str(shop.id),
                    'title': shop.title,
                    'subtitle': shop.subtitle,
                    'slug': shop.slug,
                    'description': shop.description,
                    'image': shop.image,
                    'cover': shop.cover,
                    'ordering': shop.ordering,
                    'is_promoted': shop.is_promoted,

                    'is_published': shop.is_published,
                    'created_at': shop.created_at,
                    'updated_at': shop.updated_at,
                })

            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'code': 500,
                'message': str(e),
            })

    def post(self, request):
        try:
            shop = Company()
            shop.title = request.data.get('title')
            shop.subtitle = request.data.get('subtitle')
            shop.slug = slugify(request.data.get('title'))
            shop.description = request.data.get('description')
            shop.image = request.data.get('image')
            shop.cover = request.data.get('cover')
            shop.ordering = request.data.get('ordering')
            shop.is_promoted = request.data.get('is_promoted')
            shop.is_published = request.data.get('is_published')
            shop.save()

            response = {
                'id': str(shop.id),
                'title': shop.title,
                'subtitle': shop.subtitle,
                'description': shop.description,
                'image': shop.image,
                'cover': shop.cover,
                'ordering': shop.ordering,
                'is_promoted': shop.is_promoted,
                'is_published': shop.is_published,
                'created_at': shop.created_at,
                'updated_at': shop.updated_at,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyAPIView(APIView):
    def get(self, request, slug):
        try:
            shop = Company.objects.get(slug=slug)
            response = {
                'id': str(shop.id),
                'title': shop.title,
                'subtitle': shop.subtitle,
                'slug': shop.slug,
                'description': shop.description,
                'image': shop.image,
                'cover': shop.cover,
                'ordering': shop.ordering,
                'is_promoted': shop.is_promoted,
                'is_published': shop.is_published,
                'created_at': shop.created_at,
                'updated_at': shop.updated_at,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'message': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            capture_exception(error)
            return Response({
                'code': 500,
                'message': str(error),
            })

    def put(self, request, id):
        try:
            shop = Company.objects.get(_id=ObjectId(id))
            shop.title = request.data.get('title', shop.title)
            shop.subtitle = request.data.get('subtitle', shop.subtitle)
            shop.slug = slugify(request.data.get('title', shop.title))
            shop.description = request.data.get(
                'description', shop.description)
            shop.image = request.data.get('image', shop.image)
            shop.cover = request.data.get('cover', shop.cover)
            shop.ordering = request.data.get('ordering', shop.ordering)
            shop.is_promoted = request.data.get(
                'is_promoted', shop.is_promoted)
            shop.is_published = request.data.get(
                'is_published', shop.is_published)
            shop.save()

            response = {
                'id': str(shop.id),
                'title': shop.title,
                'subtitle': shop.subtitle,
                'description': shop.description,
                'slug': shop.slug,
                'image': shop.image,
                'cover': shop.cover,
                'ordering': shop.ordering,
                'is_promoted': shop.is_promoted,
                'is_published': shop.is_published,
                'created_at': shop.created_at,
                'updated_at': shop.updated_at,
            }
            return Response(response, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'message': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            shop = Company.objects.get(_id=ObjectId(id))
            shop.delete()
            return Response({'message': 'Deleted'},
                            status=status.HTTP_204_NO_CONTENT)
        except Company.DoesNotExist:
            return Response({'message': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyRequest(APIView):
    def get(self, request, company):
        try:
            PAGE_NUMBER = int(request.GET.get('page', 1))
            PER_PAGE_LIMIT = 1
            offset = (PAGE_NUMBER - 1) * PER_PAGE_LIMIT
            response = []
            requests = Request.objects.filter(
                company=company)[offset:PER_PAGE_LIMIT]
            for order_request in requests:
                response.append(order_request_serializer(order_request))

            return Response(response, status=status.HTTP_200_OK)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanyLocationsAPIView(APIView):
    def get(self, request, company):
        try:
            response = []
            locations = Warehouse.objects.filter(company=company)
            for location in locations:
                response.append(warehouse_serializer(location))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as error:
            capture_exception(error)
            return Response({
                'message': str(error), 'code': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CompanySuppliersAPIView(APIView):
    def get(self, request, company):
        try:
            response = []
            suppliers = CompanySupplier.objects.filter(company=company)
            for supplier in suppliers:
                response.append(company_supplier_serializer(supplier))
            return Response(response, status=status.HTTP_200_OK)
        except Exception as error:
            capture_exception(error)
            return Response({
                'message': str(error), 'code': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, company):
        try:
            # TODO first check if the supplier is not already on the database
            supplier = Supplier()
            supplier.title = request.get('title')
            supplier.slug = slugify(request.get('title'))
            supplier.description = request.get('description')
            supplier.save()

            company_supplier = CompanySupplier()
            company_supplier.company = Company.objects.get(_id=ObjectId(company))
            company_supplier.supplier = Supplier.objects.get(_id=ObjectId(supplier.id))
            company_supplier.save()

            return Response({'message': 'Created', 'code': 201},
                            status=status.HTTP_200_OK)
        except Exception as error:
            capture_exception(error)
            return Response({
                'message': str(error), 'code': 500},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
