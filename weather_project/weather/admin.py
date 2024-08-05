from django.contrib import admin

from weather.models import CitySearchHistory


@admin.register(CitySearchHistory)
class CitySearchHistoryAdmin(admin.ModelAdmin):
    list_display = ["city", "search_date", "search_count"]
    list_filter = ["search_date"]
