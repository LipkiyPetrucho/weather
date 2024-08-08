import requests
import requests_cache
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3 import Retry

# Configuring Open-Meteo API client with cache and repeated requests mechanism.
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retries = Retry(
    total=5,
    backoff_factor=0.2,
    status_forcelist=[502, 503, 504],
)
cache_session.mount("https://", HTTPAdapter(max_retries=retries))


def get_weather_data(city):
    geocode_url = f"{settings.OPEN_METEO_BASE_URL}?name={city}"

    try:
        geocode_response = cache_session.get(geocode_url)
        geocode_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching geocode data: {e}")
        return None

    geocode_data = geocode_response.json()

    if "results" not in geocode_data or not geocode_data["results"]:
        return None

    latitude = geocode_data["results"][0]["latitude"]
    longitude = geocode_data["results"][0]["longitude"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,weathercode",
        "current_weather": True,
    }
    try:
        response = cache_session.get(settings.OPEN_METEO_FORECAST_URL, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

    weather_data = response.json()

    if "current_weather" not in weather_data:
        return None

    current_weather = weather_data["current_weather"]
    temperature = round(current_weather["temperature"], 1)
    weather_code = current_weather["weathercode"]
    weather_description, weather_icon = get_weather_description_and_icon(weather_code)

    return {
        "latitude": weather_data["latitude"],
        "longitude": weather_data["longitude"],
        "elevation": weather_data["elevation"],
        "timezone": weather_data["timezone"],
        "timezone_abbreviation": weather_data["timezone_abbreviation"],
        "utc_offset_seconds": weather_data["utc_offset_seconds"],
        "current_temperature": temperature,
        "weather_description": weather_description,
        "weather_icon": weather_icon,
        "city": city,
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
        99: ("Thunderstorm with heavy hail", "⛈️"),
    }

    return weather_codes.get(weather_code, ("Unknown", "❓"))
