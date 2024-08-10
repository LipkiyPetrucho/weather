from django.urls import path
from weather import views

urlpatterns = [
    path("", views.weather_view, name="weather_view"),
    path("weather/", views.weather_view, name="weather"),
]
