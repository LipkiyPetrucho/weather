import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from weather.models import CitySearchHistory


@pytest.fixture
def user(db):
    """Создает и возвращает пользователя."""
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def api_client(user):
    """Создает и возвращает клиента с аутентификацией."""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def city_data(user):
    """Возвращает данные для города."""
    return {"city": "Paris", "user": user.id, "temperature": 20.0}


def test_create_city_search_history(api_client, city_data):
    response = api_client.post("/api/search-history/", city_data)
    assert response.status_code == 201
    assert CitySearchHistory.objects.count() == 1


def test_list_city_search_history(api_client, user):
    CitySearchHistory.objects.create(user=user, city="Paris", temperature=20.0)
    response = api_client.get("/api/search-history/")
    assert response.status_code == 200
    assert len(response.data) == 1


def test_retrieve_city_search_history(api_client, user):
    city_search = CitySearchHistory.objects.create(
        user=user, city="Paris", temperature=20.0
    )
    response = api_client.get(f"/api/search-history/{city_search.id}/")
    assert response.status_code == 200
    assert response.data["city"] == "Paris"


def test_update_city_search_history(api_client, user):
    city_search = CitySearchHistory.objects.create(
        user=user, city="Paris", temperature=20.0
    )
    updated_data = {"city": "London", "temperature": 15.0, "user": user.id}
    response = api_client.put(f"/api/search-history/{city_search.id}/", updated_data)

    print(response.data)

    assert response.status_code == status.HTTP_200_OK
    city_search.refresh_from_db()
    assert city_search.city == "London"
    assert city_search.temperature == 15.0


def test_delete_city_search_history(api_client, user):
    city_search = CitySearchHistory.objects.create(
        user=user, city="Paris", temperature=20.0
    )
    response = api_client.delete(f"/api/search-history/{city_search.id}/")
    assert response.status_code == 204
    assert CitySearchHistory.objects.count() == 0


@pytest.fixture
def city_search_history(user):
    """Создает несколько записей в истории поиска."""
    CitySearchHistory.objects.create(user=user, city="Paris", temperature=20.0)
    CitySearchHistory.objects.create(user=user, city="Paris", temperature=22.0)
    CitySearchHistory.objects.create(user=user, city="London", temperature=18.0)


def test_city_search_count(api_client, city_search_history):
    response = api_client.get("/api/city-search-count/")
    assert response.status_code == 200
    assert len(response.data) == 2
    assert response.data[0]["city"] == "Paris"
    assert response.data[0]["count"] == 2
    assert response.data[1]["city"] == "London"
    assert response.data[1]["count"] == 1
