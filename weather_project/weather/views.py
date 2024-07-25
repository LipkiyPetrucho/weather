import openmeteo_requests
import requests
import requests_cache
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from openmeteo_sdk.Variable import Variable

from .models import CitySearchHistory

cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_strategy = Retry(
    total=5,
    backoff_factor=0.2,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
cache_session.mount("http://", adapter)
cache_session.mount("https://", adapter)
openmeteo = openmeteo_requests.Client(session=cache_session)

def get_weather_data(city):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geocode_response = requests.get(geocode_url)
    geocode_response.raise_for_status()
    geocode_data = geocode_response.json()

    if not geocode_data['results']:
        return None

    latitude = geocode_data['results'][0]['latitude']
    longitude = geocode_data['results'][0]['longitude']

    om = openmeteo_requests.Client()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": ["temperature_2m", "precipitation"],
        "current": ["temperature_2m"]
    }

    response = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)[0]
    current = response.Current()
    current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
    current_temperature_2m = next(
        filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))

    # Округление температуры до одного десятичного знака
    temperature = round(current_temperature_2m.Value(), 1)

    weather_data = {
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "elevation": response.Elevation(),
        "timezone": response.Timezone(),
        "timezone_abbreviation": response.TimezoneAbbreviation(),
        "utc_offset_seconds": response.UtcOffsetSeconds(),
        "current_temperature": temperature,
        "city": city
    }

    return weather_data

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