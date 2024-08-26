import requests

import requests_cache
from django.conf import settings
from requests.adapters import HTTPAdapter
from urllib3 import Retry

cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
retries = Retry(
    total=5,
    backoff_factor=0.2,
    status_forcelist=[502, 503, 504],
)
cache_session.mount("https://", HTTPAdapter(max_retries=retries))


def get_geocode_data(city):
    """Получает географические данные для указанного города."""
    language = detect_language(city)
    geocode_url = (
        f"{settings.OPEN_METEO_BASE_URL}?name={city}&count=1&language={language}"
    )
    geocode_data = fetch_data(geocode_url)
    results = geocode_data.get("results")

    if not results:
        return {"error": "Город не найден."}
    result = results[0]

    return {
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "population": "{:,}".format(result.get("population", 0)),
        "country_code": result.get("country_code"),
        "country": result.get("country"),
    }


def get_weather_data(city):
    """Получает данные о погоде для указанного города."""
    geocode_result = get_geocode_data(city)
    if "error" in geocode_result:
        return geocode_result

    latitude = geocode_result["latitude"]
    longitude = geocode_result["longitude"]
    population = geocode_result["population"]
    country_code = geocode_result["country_code"]
    country = geocode_result["country"]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "wind_speed_10m",
            "weather_code",
            "apparent_temperature",
            "wind_gusts_10m",
        ],
        "wind_speed_unit": "ms",
    }
    weather_data = fetch_data(settings.OPEN_METEO_FORECAST_URL, params)
    current_weather = weather_data["current"]
    temperature = current_weather["temperature_2m"]
    wind_speed = current_weather["wind_speed_10m"]
    weather_code = current_weather["weather_code"]
    apparent_temperature = current_weather["apparent_temperature"]
    wind_gusts_10m = current_weather["wind_gusts_10m"]
    weather_description, weather_icon = get_weather_description_and_icon(weather_code)

    return {
        "latitude": weather_data["latitude"],
        "longitude": weather_data["longitude"],
        "elevation": weather_data["elevation"],
        "timezone": weather_data["timezone"],
        "timezone_abbreviation": weather_data["timezone_abbreviation"],
        "utc_offset_seconds": weather_data["utc_offset_seconds"],
        "current_temperature": temperature,
        "current_apparent_temperature": apparent_temperature,
        "current_wind_speed": wind_speed,
        "current_wind_gusts": wind_gusts_10m,
        "weather_description": weather_description,
        "weather_icon": weather_icon,
        "city": city,
        "population": population,
        "country_code": country_code,
        "country": country,
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


def detect_language(city):
    if any("а" <= char <= "я" or "А" <= char <= "Я" for char in city):
        return "ru"
    else:
        return "en"


def fetch_data(url, params=None):
    """Функция для получения данных с обработкой ошибок."""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"error": "Не удалось получить данные."}
