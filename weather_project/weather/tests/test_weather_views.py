import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from weather.models import CitySearchHistory
from dotenv import load_dotenv

# Подключаемся к базе данных для тестов
pytestmark = pytest.mark.django_db
load_dotenv()  # Загружаем переменные окружения из .env файла


# Фикстура для создания пользователя
@pytest.fixture
def user(client):
    # Создаем пользователя для тестов
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")  # Авторизуем пользователя
    return user


def test_get_weather_view(client, user):
    # Тестируем GET запрос к представлению погоды
    response = client.get(reverse("weather_view"))
    assert response.status_code == 200
    assert "Enter a city name to see the weather." in response.content.decode()


def test_post_weather_view(client, user):
    # Тестируем POST запрос с корректным городом
    response = client.post(reverse("weather_view"), {"city": "Paris"})
    assert response.status_code == 200
    assert CitySearchHistory.objects.filter(
        city="Paris"
    ).exists()  # Проверяем, что город сохраняется


def test_weather_view_invalid_city(client, user):
    # Тестируем POST запрос с некорректным городом
    response = client.post(reverse("weather_view"), {"city": "InvalidCity"})
    assert response.status_code == 200
    assert (
        "Не удалось найти данные о погоде для введенного города."
        in response.content.decode()
    )  # Проверяем отображение ошибки
