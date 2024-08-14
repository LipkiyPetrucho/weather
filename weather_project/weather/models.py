from deep_translator import GoogleTranslator
from django.db import models
from django.contrib.auth.models import User


class CitySearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    search_date = models.DateTimeField(auto_now_add=True)
    last_searched = models.DateTimeField(auto_now=True)
    temperature = models.FloatField(default=18.0)

    def save(self, *args, **kwargs):
        if isinstance(self.city, str):
            self.city = (
                GoogleTranslator(source="ru", target="en").translate(self.city).title()
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city} on {self.search_date}"
