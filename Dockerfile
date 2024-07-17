FROM python:3.11-slim

COPY requirements.txt requirements.txt
COPY weather /weather

WORKDIR /weather
EXPOSE 8000

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "weather_project.wsgi:application"]
