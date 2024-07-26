import openmeteo_requests
import requests
import requests_cache
from retry_requests import retry
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from openmeteo_sdk.Variable import Variable

from .models import CitySearchHistory

# Настройка клиента Open-Meteo API с кешем и механизмом повторных запросов
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather_data(city):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geocode_response = retry_session.get(geocode_url)
    geocode_response.raise_for_status()
    geocode_data = geocode_response.json()

    if not geocode_data['results']:
        return None

    latitude = geocode_data['results'][0]['latitude']
    longitude = geocode_data['results'][0]['longitude']

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,weathercode",
        "current_weather": True
    }

    response = retry_session.get("https://api.open-meteo.com/v1/forecast", params=params)
    response.raise_for_status()
    weather_data = response.json()

    if 'current_weather' not in weather_data:
        return None

    current_weather = weather_data['current_weather']
    temperature = round(current_weather['temperature'], 1)
    weather_code = current_weather['weathercode']
    weather_description, weather_icon = get_weather_description_and_icon(weather_code)

    return {
        "latitude": weather_data['latitude'],
        "longitude": weather_data['longitude'],
        "elevation": weather_data['elevation'],
        "timezone": weather_data['timezone'],
        "timezone_abbreviation": weather_data['timezone_abbreviation'],
        "utc_offset_seconds": weather_data['utc_offset_seconds'],
        "current_temperature": temperature,
        "weather_description": weather_description,
        "weather_icon": weather_icon,
        "city": city
    }

def get_weather_description_and_icon(weather_code):
    weather_codes = {
        0: ("Clear sky", "☀️"),
        1: ("Mainly clear", "🌤️"),
        2: ("Partly cloudy", "⛅"),
        3: ("Overcast", "☁️"),
        45: ("Fog", "🌫️"),
        48: ("Depositing rime fog", "🌫️"),
        51: ("Drizzle: Light", "🌦️"),
        53: ("Drizzle: Moderate", "🌧️"),
        55: ("Drizzle: Dense intensity", "🌧️"),
        56: ("Freezing Drizzle: Light", "🌨️"),
        57: ("Freezing Drizzle: Dense intensity", "🌨️"),
        61: ("Rain: Slight", "🌧️"),
        63: ("Rain: Moderate", "🌧️"),
        65: ("Rain: Heavy intensity", "🌧️"),
        66: ("Freezing Rain: Light", "🌨️"),
        67: ("Freezing Rain: Heavy intensity", "🌨️"),
        71: ("Snow fall: Slight", "🌨️"),
        73: ("Snow fall: Moderate", "🌨️"),
        75: ("Snow fall: Heavy intensity", "🌨️"),
        77: ("Snow grains", "🌨️"),
        80: ("Rain showers: Slight", "🌧️"),
        81: ("Rain showers: Moderate", "🌧️"),
        82: ("Rain showers: Violent", "🌧️"),
        85: ("Snow showers: Slight", "🌨️"),
        86: ("Snow showers: Heavy", "🌨️"),
        95: ("Thunderstorm: Slight or moderate", "⛈️"),
        96: ("Thunderstorm with slight hail", "⛈️"),
        99: ("Thunderstorm with heavy hail", "⛈️")
    }

    return weather_codes.get(weather_code, ("Unknown", "❓"))

@login_required
@csrf_exempt
def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        request.session['last_city'] = city
        weather_data = get_weather_data(city)
        if weather_data is not None:
            track_search(request, weather_data['current_temperature'])
    else:
        city = request.GET.get('city', 'Paris')
        weather_data = get_weather_data(city)

    if weather_data is None:
        return render(request, 'error.html', {"message": "City not found"})

    recent_cities = CitySearchHistory.objects.filter(user=request.user).order_by('-search_date')[:5]

    last_city = request.session.get('last_city')
    if last_city:
        message = f"Do you want to see the weather in {last_city} again?"
    else:
        message = "Enter a city name to see the weather."

    return render(request, 'weather.html', {
        "weather_data": weather_data,
        "recent_cities": recent_cities,
        "city": city,
        "message": message,
        "last_city": last_city,
    })


def autocomplete(request):
    if 'term' in request.GET:
        qs = CitySearchHistory.objects.filter(city__icontains=request.GET.get('term')).distinct()
        cities = list(qs.values_list('city', flat=True))
        return JsonResponse(cities, safe=False)
    return JsonResponse([], safe=False)

@login_required
def track_search(request, temperature):
    if request.method == 'POST':
        city = request.POST.get('city')
        user = request.user

        # Creating a new entry in the search history
        CitySearchHistory.objects.create(user=user, city=city, temperature=temperature, search_date=timezone.now())

        # Update a record to count the number of searches
        search_history = CitySearchHistory.objects.filter(user=user, city=city)
        if search_history.exists():
            search_record = search_history.latest('search_date')
            search_record.search_count += 1
            search_record.temperature = temperature
            search_record.save()
        else:
            CitySearchHistory.objects.create(user=user, city=city, temperature=temperature, search_count=1)

        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)

def search_statistics(request):
    stats = CitySearchHistory.objects.values('city').annotate(count=Count('city')).order_by('-count')
    return JsonResponse(list(stats), safe=False)

@login_required
def search_history(request):
    history = CitySearchHistory.objects.filter(user=request.user).order_by('-search_date')
    return render(request, 'search_history.html', {'history': history})

@login_required
def get_city_search_count(request):
    if request.method == 'GET':
        city_counts = CitySearchHistory.objects.values('city').annotate(search_count=Count('city')).order_by('-search_count')
        return JsonResponse(list(city_counts), safe=False)
    return JsonResponse({'status': 'error'}, status=400)