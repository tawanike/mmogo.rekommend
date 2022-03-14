from rest_framework import serializers
from mmogo.contrib.categories.models import Category

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
    class Meta:
        model= Category
        fields = '__all__'
