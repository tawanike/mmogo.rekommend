from rest_framework import status
from bson.objectid import ObjectId
from sentry_sdk import capture_exception
from rest_framework.views import APIView
from rest_framework.response import Response
from mmogo.contrib.ratings.models import Rating
from mmogo.contrib.ratings.serializer import rating_serializer
from mmogo.contrib.products.serializers import product_serializer


class RatingsAPIView(APIView):
    def get(self, request, user, object_type, object_id):
        try:
            print('PANO')
            ratings = Rating.objects.get(
                user=user, object_type=object_type, object_id=object_id, is_deleted__in=[False])
            response = rating_serializer(ratings)
            return Response(response, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return Response({'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RateAPIView(APIView):
    def post(self, request):

        try:
            rating = Rating.objects.get(user=request.data.get('user'),
                                        object_type=request.data.get(
                                            'object_type'),
                                        object_id=request.data.get(
                                            'object_id'),
                                        is_deleted__in=[False])

            rating.rating = request.data.get('rating')
            rating.save()
            return Response({'message': 'Created', 'code': 201},
                            status=status.HTTP_201_CREATED)
        except Rating.DoesNotExist:
            rating = Rating()
            rating.user = request.data.get('user')
            rating.is_deleted = False
            rating.rating = request.data.get('rating')
            rating.object_id = request.data.get('object_id')
            rating.object_type = request.data.get('object_type')
            rating.save()

            ratings = Rating.objects.get(_id=rating.id, is_deleted__in=[False])
            response = {
                "user": str(ratings.user),
                "object_type": ratings.object_type,
                "object_id": ratings.object_id,
                "rating": ratings.rating
            }

            return Response(response,
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
