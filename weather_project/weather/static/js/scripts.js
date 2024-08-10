//$(function() {
//    var token = "deb5c7c3f11a7c507c9b555a43ee9a58c493c8b8";
//
//    function formatResult(value, currentValue, suggestion, options) {
//        var newValue = suggestion.data.city;
//        suggestion.value = newValue;
//        return $.Suggestions.prototype.formatResult.call(this, newValue, currentValue, suggestion, options);
//    }
//
//    function formatSelected(suggestion) {
//        return suggestion.data.city;
//    }
//
//    $("#id_city").suggestions({
//        token: token,
//        type: "ADDRESS",
//        hint: false,
//        bounds: "city",
//        language: "en",
//        geoLocation: false,
//        enrichmentEnabled: false,
//        constraints: {
//            locations: { country: "*" }
//        },
//        formatResult: formatResult,
//        formatSelected: formatSelected,
//        onSelect: function(suggestion) {
//            console.log(suggestion);
//        }
//    });
//});

function getWeatherForLastCity(button) {
    const city = button.getAttribute('data-last-city');
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = button.getAttribute('data-url');
    const csrfToken = '{{ csrf_token }}';
    const csrfInput = document.createElement('input');
    csrfInput.type = 'hidden';
    csrfInput.name = 'csrfmiddlewaretoken';
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    const cityInput = document.createElement('input');
    cityInput.type = 'hidden';
    cityInput.name = 'city';
    cityInput.value = city;
    form.appendChild(cityInput);

    document.body.appendChild(form);
    form.submit();
}

//получение статистики по числу поисков городов
function fetchCitySearchCounts() {
    $.ajax({
        url: "{% url 'city_search_count' %}",
        method: "GET",
        success: function(data) {
            const countsDiv = document.getElementById('city-search-counts');
            countsDiv.innerHTML = '<ul>' + data.map(item => `<li>${item.city}: ${item.search_count}</li>`).join('') + '</ul>';
        },
        error: function(error) {
            console.error("Error fetching city search counts:", error);
        }
    });
}

//GeoNames
$(document).ready(function() {
    $('#id_city').on('input', function() {
        let query = $(this).val();

        // Проверка, что введённый текст не пустой
        if (query.length < 2) {
            $('#suggestions').empty();
            return;
        }

        // Определяем язык
        let lang = 'en';
        if (/[а-яА-ЯЁё]/.test(query)) {
        lang = 'ru';
        }

        // Показать индикацию загрузки
        $('#suggestions').html('<div class="loading">Загрузка...</div>');

        // AJAX запрос к GeoNames API
        $.ajax({
            url: 'http://api.geonames.org/search',
            type: 'GET',
            dataType: 'json',
            data: {
                q: query,
                maxRows: 10, // кол-во результатов
                username: 'petr_lip',
                type: 'json',
                lang: lang,
            },
            success: function(data) {
                $('#suggestions').empty();

                // Функция для создания текста подсказки
                function createSuggestionText(cityData) {
                    const cityName = cityData.name;
                    const countryName = cityData.country || '';  // Если country отсутствует, добавляется пустая строка

                    // Склеиваем название города и страны, если страна доступна
                    return countryName ? `${cityName}, ${countryName}` : cityName;
                }

                // Отображение подсказок
                if (data.geonames && data.geonames.length > 0) {
                    // Сохранение данных в localStorage
                    localStorage.setItem('lastSearchResults', JSON.stringify(data.geonames));

                    data.geonames.forEach(function(city) {
                        const suggestionText = createSuggestionText(city);
                        $('#suggestions').append(`<div class="suggestion" data-name="${city.name}">${suggestionText}</div>`);
                    });


                    // Обработка клика по подсказке
                    $('.suggestion').on('click', function() {
                        $('#id_city').val($(this).data('name'));
                        $('#suggestions').empty();
                    });
                }
            },
            error: function() {
                $('#suggestions').text('Ошибка запроса');
            }
        });
    });
});

