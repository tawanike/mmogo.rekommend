from rest_framework import serializers
from mmogo.contrib.locations.models import Province, Country, City



class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'title', 'subtitle', 'slug', 'description',
                  'image')


class ProvinceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Province
        fields = ('id', 'title', 'subtitle', 'slug', 'description',
                  'image', 'ordering')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'title', 'subtitle', 'slug', 'description',
                  'image', 'ordering')