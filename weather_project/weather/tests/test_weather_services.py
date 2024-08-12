import pytest
import requests
from weather.services import get_weather_data

from pytest_mock import MockFixture


def test_get_weather_data_success(mocker: MockFixture) -> None:
    """Тест успешного получения данных о погоде."""
    mock_geocode_response = mocker.Mock()
    mock_geocode_response.json.return_value = {
        "results": [
            {
                "latitude": 50.0755,
                "longitude": 14.4378,
                "population": 1300000,
                "country_code": "CZ",
                "country": "Czech Republic",
            }
        ]
    }
    mock_geocode_response.raise_for_status.return_value = None

    mock_weather_response = mocker.Mock()
    mock_weather_response.json.return_value = {
        "latitude": 50.0755,
        "longitude": 14.4378,
        "current": {
            "temperature_2m": 20,
            "wind_speed_10m": 3.5,
            "weather_code": 1,
            "apparent_temperature": 19,
            "wind_gusts_10m": 5.5,
        },
        "elevation": 300,
        "timezone": "Europe/Prague",
        "timezone_abbreviation": "CET",
        "utc_offset_seconds": 3600,
    }
    mock_weather_response.raise_for_status.return_value = None

    mock_session = mocker.patch(
        "weather.services.cache_session.get",
        side_effect=[mock_geocode_response, mock_weather_response],
    )

    result = get_weather_data(city="Prague")

    assert mock_session.call_count == 2
    assert result == {
        "latitude": 50.0755,
        "longitude": 14.4378,
        "elevation": 300,
        "timezone": "Europe/Prague",
        "timezone_abbreviation": "CET",
        "utc_offset_seconds": 3600,
        "current_temperature": 20,
        "current_apparent_temperature": 19,
        "current_wind_speed": 3.5,
        "current_wind_gusts": 5.5,
        "weather_description": "Mainly clear",
        "weather_icon": "🌤️",
        "city": "Prague",
        "population": "1,300,000",
        "country_code": "CZ",
        "country": "Czech Republic",
    }


def test_get_weather_data_failure(mocker: MockFixture) -> None:
    """Тест на случай неудачного запроса."""
    mock_geocode_response = mocker.Mock()
    mock_geocode_response.raise_for_status.side_effect = requests.RequestException

    mocker.patch(
        "weather.services.cache_session.get", return_value=mock_geocode_response
    )

    result = get_weather_data(city="NonexistentCity")
    assert result is None


def test_get_weather_data_empty_results(mocker: MockFixture) -> None:
    """Тест на случай, если геокодирование не нашло результатов."""
    mock_geocode_response = mocker.Mock()
    mock_geocode_response.json.return_value = {"results": []}
    mock_geocode_response.raise_for_status.return_value = None

    mocker.patch(
        "weather.services.cache_session.get", return_value=mock_geocode_response
    )

    result = get_weather_data(city="EmptyCity")
    assert result is None


@pytest.mark.parametrize(
    "city, language",
    [("Москва", "ru"), ("Prague", "en"), ("北京", "en")],
)
def test_detect_language(city: str, language: str) -> None:
    """Тест функции detect_language для разных городов."""
    from weather.services import detect_language

    result = detect_language(city)
    assert result == language
