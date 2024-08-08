from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from weather import views
from weather.views import CitySearchCountViewSet

router = DefaultRouter()
router.register(r'search-history', views.CitySearchHistoryViewSet, basename='search-history')
router.register(r'city-search-count', CitySearchCountViewSet, basename='city-search-count')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("weather.urls")),
    path('api/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
