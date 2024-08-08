from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import CitySearchHistory

class CitySearchHistoryTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_city_search_history(self):
        url = reverse('search-history')
        data = {'city': 'Paris', 'temperature': 20.0}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_city_search_count(self):
        CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=20.0)
        CitySearchHistory.objects.create(user=self.user, city='London', temperature=15.0)
        url = reverse('city-search-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
