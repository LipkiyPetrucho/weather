from django.urls import path, include
from rest_framework.routers import DefaultRouter

from weather.api import views

router = DefaultRouter()
router.register(
    r"search-history", views.CitySearchHistoryViewSet, basename="search-history"
)
router.register(
    r"city-search-count", views.CitySearchCountViewSet, basename="city-search-count"
)

urlpatterns = [
    path("", include(router.urls)),
]
