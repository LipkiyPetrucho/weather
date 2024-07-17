import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import CitySearchHistory


def get_weather_data(city):
    api_url = f'https://api.open-meteo.com/v1/forecast?city={
        city}&hourly=temperature_2m'
    response = requests.get(api_url)
    return response.json()


@login_required
def weather_view(request):
    city = request.GET.get('city')
    weather_data = None
    if city:
        weather_data = get_weather_data(city)
        CitySearchHistory.objects.create(user=request.user, city=city)

    recent_cities = CitySearchHistory.objects.filter(
        user=request.user).order_by('-search_date')[:5]

    return render(request,
                  'weather/weather.html',
                  {'weather_data': weather_data,
                   'recent_cities': recent_cities})

def autocomplete(request):
    if 'term' in request.GET:
        qs = CitySearchHistory.objects.filter(city__icontains=request.GET.get('term'))
        cities = list(qs.values_list('city', flat=True).distinct())
        return JsonResponse(cities, safe=False)
    return JsonResponse([], safe=False)
