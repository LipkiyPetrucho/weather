$(function() {
    $("#city").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "/autocomplete/",
                data: { term: request.term },
                success: function(data) {
                    response(data);
                }
            });
        },
        minLength: 2,
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
