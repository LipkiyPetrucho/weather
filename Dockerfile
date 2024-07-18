FROM python:3.11-slim

COPY weather_project/requirements.txt requirements.txt
COPY weather_project /weather_project

WORKDIR /weather_project
EXPOSE 8000

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "weather_project.wsgi:application"]
