from django.urls import path
from .views import (weather_view, autocomplete, track_search,
                    search_statistics, search_history, city_search_count_view,)

urlpatterns = [
    path('', weather_view, name='weather_view'),
    path('weather/', weather_view, name='weather'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('track_search/', track_search, name='track_search'),
    path('search_statistics/', search_statistics, name='search_statistics'),
    path('search_history/', search_history, name='search_history'),
    path('city_search_count/', city_search_count_view, name='city_search_count'),
]
