from django.db.models import Count
from rest_framework import viewsets
from rest_framework.response import Response

from weather.api.serializers import CitySearchHistorySerializer, CitySearchStatsSerializer
from weather.models import CitySearchHistory


class CitySearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = CitySearchHistory.objects.all()
    serializer_class = CitySearchHistorySerializer

class CitySearchCountViewSet(viewsets.ViewSet):
    queryset = CitySearchHistory.objects.all()
    serializer_class = CitySearchStatsSerializer

    def list(self, request):
        stats = self.queryset.values('city').annotate(count=Count('city')).order_by('-count')
        serializer = self.serializer_class(stats, many=True)
        return Response(serializer.data)