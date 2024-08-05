from django.urls import path
from weather.views import (
    weather_view,
    track_search,
    search_statistics,
    search_history,
    city_search_count,
)

urlpatterns = [
    path("", weather_view, name="weather_view"),
    path("weather/", weather_view, name="weather"),
    path("track_search/", track_search, name="track_search"),
    path("search_statistics/", search_statistics, name="search_statistics"),
    path("search_history/", search_history, name="search_history"),
    path("city_search_count/", city_search_count, name="city_search_count"),
]
