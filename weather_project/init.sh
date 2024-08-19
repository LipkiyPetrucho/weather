#!/bin/bash
set -e

#python ./manage.py collectstatic --noinput
python ./manage.py makemigrations --noinput
python ./manage.py migrate --noinput
poetry run gunicorn --bind 0.0.0.0:8000 weather_project.wsgi:application --timeout 120