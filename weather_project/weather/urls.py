from django.urls import path
from weather import views

urlpatterns = [
    path("", views.weather_view, name="weather_view"),
    path("weather/", views.weather_view, name="weather"),
    path("search_statistics/", views.search_statistics, name="search_statistics"),
    path("search_history/", views.search_history, name="search_history"),
    path("city_search_count/", views.city_search_count, name="city_search_count"),
]
