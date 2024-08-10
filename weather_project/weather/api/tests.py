from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from weather.models import CitySearchHistory

class CitySearchHistoryViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.city_data = {'city': 'Paris', 'user': self.user.id, 'temperature': 20.0}

    def test_create_city_search_history(self):
        response = self.client.post('/api/search-history/', self.city_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CitySearchHistory.objects.count(), 1)

    def test_list_city_search_history(self):
        CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=20.0)
        response = self.client.get('/api/search-history/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_city_search_history(self):
        city_search = CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=20.0)
        response = self.client.get(f'/api/search-history/{city_search.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['city'], 'Paris')

    def test_update_city_search_history(self):
        city_search = CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=20.0)
        updated_data = {'city': 'London', 'temperature': 15.0, 'user': self.user.id}
        response = self.client.put(f'/api/search-history/{city_search.id}/', updated_data)

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        city_search.refresh_from_db()
        self.assertEqual(city_search.city, 'London')
        self.assertEqual(city_search.temperature, 15.0)

    def test_delete_city_search_history(self):
        city_search = CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=20.0)
        response = self.client.delete(f'/api/search-history/{city_search.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CitySearchHistory.objects.count(), 0)

class CitySearchCountViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=20.0)
        CitySearchHistory.objects.create(user=self.user, city='Paris', temperature=22.0)
        CitySearchHistory.objects.create(user=self.user, city='London', temperature=18.0)

    def test_city_search_count(self):
        response = self.client.get('/api/city-search-count/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['city'], 'Paris')
        self.assertEqual(response.data[0]['count'], 2)
        self.assertEqual(response.data[1]['city'], 'London')
        self.assertEqual(response.data[1]['count'], 1)

