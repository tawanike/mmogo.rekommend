from rest_framework import serializers

from commace.stores.models import Store


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            'id', 'title', 'slug', 'description', 'image', 'cover', 
            'subtitle', 'links', 'published', 'featured', 'ordering']
