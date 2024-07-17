from django.urls import path
from .views import weather_view, autocomplete

urlpatterns = [
    path('', weather_view, name='weather_view'),
    path('autocomplete/', autocomplete, name='autocomplete'),
]
