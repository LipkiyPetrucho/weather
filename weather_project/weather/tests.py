from django.test import TestCase
from django.contrib.auth.models import User
from weather.models import CitySearchHistory


class CitySearchHistoryTests(TestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_create_city_search_history(self):
        """
        Тест создания новой записи о поиске города.
        """
        self.client.login(username="testuser", password="testpass")
        url = "/search_history/"
        data = {"city": "Paris", "temperature": 20.0}

        response = self.client.post(url, data, format="json")

        # Проверяем статус ответа
        self.assertEqual(
            response.status_code,
            200,
            msg=f"Response status code: {response.status_code}, content: {response.content}",
        )

        # Проверяем, что запись была создана
        self.assertEqual(CitySearchHistory.objects.count(), 1)
        self.assertEqual(CitySearchHistory.objects.first().city, "Paris")

    def test_city_search_count(self):
        """
        Тест подсчёта количества поисков городов.
        """
        CitySearchHistory.objects.create(user=self.user, city="Paris", temperature=20.0)
        self.assertEqual(CitySearchHistory.objects.count(), 1)
