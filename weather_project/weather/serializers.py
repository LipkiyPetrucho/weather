from rest_framework import serializers

from weather.models import CitySearchHistory


class CitySearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CitySearchHistory
        fields = ['user', 'city', 'temperature', 'search_date']

class CitySearchStatsSerializer(serializers.Serializer):
    city = serializers.CharField()
    count = serializers.IntegerField()