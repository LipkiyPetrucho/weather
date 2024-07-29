from django.forms import ModelForm, TextInput

from .models import CitySearchHistory

class CityForm(ModelForm):
    class Meta:
        model = CitySearchHistory
        fields = ['city']
        widgets = {'city': TextInput(attrs={'class': 'form-control mr-2',
                                            'placeholder': 'Enter city name',
                                            'name': 'city',
                                            'id': 'id_city',
                                            'autocomplete': 'off',
                                            })}
