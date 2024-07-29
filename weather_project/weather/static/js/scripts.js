$(function() {
    var token = "deb5c7c3f11a7c507c9b555a43ee9a58c493c8b8";

    function formatResult(value, currentValue, suggestion, options) {
        var newValue = suggestion.data.city;
        suggestion.value = newValue;
        return $.Suggestions.prototype.formatResult.call(this, newValue, currentValue, suggestion, options);
    }

    function formatSelected(suggestion) {
        return suggestion.data.city;
    }

    $("#id_city").suggestions({
        token: token,
        type: "ADDRESS",
        hint: false,
        bounds: "city",
        language: "en",
        geoLocation: false,
        enrichmentEnabled: false,
        constraints: {
            locations: { country: "*" }
        },
        formatResult: formatResult,
        formatSelected: formatSelected,
        onSelect: function(suggestion) {
            console.log(suggestion);
        }
    });
});

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
