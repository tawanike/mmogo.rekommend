import random
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from mmogo.recommend.engine import ContentBasedEngine

class RecommendAPIView(APIView):

    def post(self, request):
        data = []
        recommended = []

        response = requests.get('https://api.zowzow.co/v1/dresses')
        print(response.status_code)
        if response.status_code < 400:
            for dress in response.json():
                data.append({
                    'id': str(dress.get('_id')),
                    'title': dress.get('title'),
                    'designer': dress.get('designer'),
                    'description': dress.get('description'),
                    'colour': dress.get('colour'),
                    'sizes': dress.get('sizes'),
                    'category': dress.get('category'),
                    'price_range': dress.get('price_range'),
                    'silhouette': dress.get('silhouette'),
                    'neckline': dress.get('neckline'),
                    'fabric': dress.get('fabric'),
                    'style': dress.get('style'),
                    'dress_type': dress.get('dress_type'),
                    'image': dress.get('image'),
                    'domain': dress.get('domain'),
                    'url': dress.get('url'),
                    'tags': dress.get('tags'),
                })
            recommend = ContentBasedEngine(data)
            if request.data.get('event') == 'like':
                sort_order = True
            else:
                sort_order = False
            
            recommendations = recommend.get_recommendations(request.data.get('item'), sort_order)
            response = requests.post('https://api.zowzow.co/v1/dresses/recommendations', json=recommendations)
            for item in response.json():
                recommended.append({
                    'id': str(item.get('_id')),
                    'title': item.get('title'),
                    'designer': item.get('designer'),
                    'description': item.get('description'),
                    'colour': item.get('colour'),
                    'sizes': item.get('sizes'),
                    'category': item.get('category'),
                    'price_range': item.get('price_range'),
                    'silhouette': item.get('silhouette'),
                    'neckline': item.get('neckline'),
                    'fabric': item.get('fabric'),
                    'style': item.get('style'),
                    'dress_type': item.get('dress_type'),
                    'image': item.get('image'),
                    'domain': item.get('domain'),
                    'url': item.get('url'),
                    'tags': item.get('tags'),
                })
            
            return Response(random.choice(recommended), status=status.HTTP_200_OK)
        return Response({"message": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)