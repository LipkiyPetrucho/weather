from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from weather.forms import CityForm
from weather.models import CitySearchHistory
from weather.redis_helper import increment_city_search_count, get_top_cities
from weather.services import get_weather_data


@csrf_exempt
def weather_view(request):
    form = CityForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        city = form.cleaned_data["city"]
        request.session["last_city"] = city
        weather_data = get_weather_data(city)
        if weather_data is not None:
            CitySearchHistory.objects.create(
                user=request.user,
                city=city,
                temperature=weather_data["current_temperature"],
                search_date=timezone.now(),
            )
            increment_city_search_count(city)
        else:
            error_message = "Не удалось найти данные о погоде для введенного города. Проверьте правильность написания."
            return render(request, "error.html", {"message": error_message})
    else:
        city = request.GET.get("city", "Paris")
        weather_data = get_weather_data(city)

    if weather_data is None:
        error_message = "Данные о погоде не найдены для данного города."
        return render(request, "error.html", {"message": error_message})

    form = CityForm()

    recent_cities = CitySearchHistory.objects.filter(user=request.user).order_by(
        "-search_date"
    )[:5]
    last_city = request.session.get("last_city")

    if last_city:
        message = f"Do you want to see the weather in {last_city} again?"
    else:
        message = "Enter a city name to see the weather."

    context = {
        "weather_data": weather_data,
        "recent_cities": recent_cities,
        "city": city,
        "message": message,
        "last_city": last_city,
        "form": form,
    }

    return render(request, "weather.html", context)


def search_history(request):
    history = CitySearchHistory.objects.filter(user=request.user).order_by(
        "-search_date"
    )
    return render(request, "search_history.html", {"history": history})


def city_search_count(request):
    top_cities = get_top_cities()
    data = [
        {"city": city.decode("utf-8"), "search_count": int(count)}
        for city, count in top_cities
    ]
    return JsonResponse(data, safe=False)
