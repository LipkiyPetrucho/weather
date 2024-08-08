from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("weather.urls")),
    path("api/", include("weather.api.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
