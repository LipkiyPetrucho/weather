from django.test import TestCase

from django.urls import reverse
from django.contrib.auth.models import User

from weather.models import CitySearchHistory


class WeatherViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = self.client_class()
        self.client.login(username='testuser', password='testpass')

    def test_get_weather_view(self):
        response = self.client.get(reverse('weather_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a city name to see the weather.")

    def test_post_weather_view(self):
        response = self.client.post(reverse('weather_view'), {'city': 'Paris'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CitySearchHistory.objects.filter(city='Paris').exists())

    def test_weather_view_invalid_city(self):
        response = self.client.post(reverse('weather_view'), {'city': 'InvalidCity'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Не удалось найти данные о погоде для введенного города.")
