from mmogo.contrib.products.models import Product
from rest_framework import status
from bson.objectid import ObjectId
from sentry_sdk import capture_exception
from rest_framework.views import APIView
from rest_framework.response import Response
from mmogo.contrib.likes.models import Like
from mmogo.contrib.likes.serializer import likes_serializer
from mmogo.contrib.products.serializers import product_serializer


class LikesAPIView(APIView):
    def get(self, request, user):
        try:
            likes = Like.objects.get(user=user, is_deleted__in=[False])
            response = likes_serializer(likes)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, user):
        try:
            like = Like.objects.get(_id=ObjectId(user))
            like.is_deleted = True
            like.save()

            return Response({'message': 'Deleted', 'code': 204},
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeAPIView(APIView):
    def post(self, request):
        try:
            Like.objects.get(user=request.data.get('user'),
                             product=request.data.get('product'), is_deleted__in=[False])
            return Response({'message': 'You have like this product already.', 'code': 409},
                            status=status.HTTP_409_CONFLICT)
        except Like.DoesNotExist:
            like = Like()
            like.user = request.data.get('user')
            like.is_deleted = False
            like.product = Product.objects.get(_id=ObjectId(request.data.get('product')))
            like.save()

            try:
                response = []
                likes = Like.objects.filter(user=request.data.get('user'), is_deleted__in=[False])
                
                for like in likes:
                    response.append(likes_serializer(like))

                return Response({
                    'count': len(likes),
                    'results': response
                }, status=status.HTTP_200_OK)

            except Exception as error:
                capture_exception(error)
                return Response({'message': str(error), 'code': 500},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Created', 'code': 201},
                            status=status.HTTP_201_CREATED)
        except Exception as error:
            capture_exception(error)
            return Response({'message': str(error)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
