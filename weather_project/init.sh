#!/bin/bash
python ./manage.py migrate
poetry run gunicorn --bind 0.0.0.0:8000 weather_project.wsgi:application --timeout 120