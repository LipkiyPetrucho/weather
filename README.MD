## Django-приложение, которое отображает прогноз погоды для заданного города.

### Стек технологий:

 - ![alt text](https://img.shields.io/badge/Python-3.12-grey?style=plastic&logo=python&logoColor=white&labelColor=%233776AB)

 - ![alt text](https://img.shields.io/badge/Django-5.0.7-grey?style=plastic&logo=django&logoColor=white&labelColor=%23092E20)

 - ![alt text](https://img.shields.io/badge/PostgreSQL-16.3-grey?style=plastic&logo=postgresql&logoColor=white&labelColor=%234169E1)

 - ![alt text](https://img.shields.io/badge/Docker-v25.0.3-grey?style=plastic&logo=docker&logoColor=white&labelColor=2496ED)

### Описание проекта
Разработано Django-приложение, которое отображает прогноз погоды для заданного города.

При запросе города http://localhost:8000/weather/ либо http://127.0.0.1:8000/weather/
```json
{
    "city": "Paris"
}
```

***

### Запуск через консоль

<details>
<summary>Для запуска через консоль необходимо:</summary>

- Клонировать проект на собственный диск в новом каталоге
  - Создать виртуальное окружение
  - Установить зависимости командой:
    ```python
    pip install poetry
    poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root 
    ```
    
<details>
<summary>Прописать переменные окружения в файле `.env.sample`. Необходимо переименовать `.env.sample` в `.env`! </summary>
   
```dotenv
SECRET_KEY='Секретный ключ Django'
DEBUG='True/False', например: True

# PostgreSQL
POSTGRES_DB_NAME='Название базы данных', например: 'name_of_db' или 'sdk_weather'
POSTGRES_DB_USER='Пользователь базы данных', например: 'db_user' или 'postgres'
POSTGRES_DB_PASSWORD='Пароль пользователя базы данных', например: 'your_password'
POSTGRES_DB_HOST='Хост базы данных', например: '127.0.0.1' или 'localhost' или 'database' для Docker
POSTGRES_DB_PORT='Порт базы данных', например: '5432'

```
</details>

<details>
<summary>Создать базу данных (в данном проекте используется PostgreSQL)</summary>

```python
psql -U postgres
create database weather;
\q
```
</details>

- Применить миграции командой:
    ```python
    poetry run python manage.py migrate
    ```

<details>
<summary>Для запуска сервера через терминал:</summary>

- Запустить сервер
    ```python
    poetry run python manage.py runserver
    ```
</details>

<details>
<summary>Для создания тестового пользователя - администратор:</summary>


- Cоздать суперпользователя
    ```python
    python manage.py createsuperuser
    ```
- ввести логин, например admin
- почту(опционально)
- ввести пароль, например admin

 зайти на http://127.0.0.1:8000/admin/ либо http://localhost:8000/admin/
- login: admin
- password: admin
</details>

</details>

***

### Запуск через Docker

<details>
<summary>Для запуска через Docker необходимо:</summary>

- Клонировать проект на собственный диск в новом каталоге
-  <details>
   <summary>Прописать переменные окружения в файле `.env.sample`. Имя файла необходимо заменить на .env!</summary>
   
    ```dotenv
    SECRET_KEY='Секретный ключ Django'
    DEBUG='True/False', например: True
    
    # PostgreSQL
    POSTGRES_DB_NAME='Название базы данных', например: 'name_of_db' или 'sdk_weather'
    POSTGRES_DB_USER='Пользователь базы данных', например: 'db_user' или 'postgres'
    POSTGRES_DB_PASSWORD='Пароль пользователя базы данных', например: 'your_password'
    POSTGRES_DB_HOST='Хост базы данных', например: '127.0.0.1' или 'localhost' или 'database' для Docker
    POSTGRES_DB_PORT='Порт базы данных', например: '5432'

    ```
   </details>

- Ввести в терминале команду:
    ```python
    docker-compose up --build
    ```
    > Происходит сборка образа контейнера согласно инструкции в файле Dockerfile и последовательный запуск всех контейнеров согласно инструкции в файле docker-compose.yaml

<details>
<summary>Для создания тестового пользователя - администратор:</summary>


- Cоздать суперпользователя
    ```python
    docker-compose run --rm <имя_сервиса> "python manage.py createsuperuser"
  например
  docker-compose run --rm web "python manage.py createsuperuser"
    ```
- ввести логин, например admin
- почту(опционально)
- ввести пароль, например admin

 зайти на http://127.0.0.1:8000/admin/ либо http://localhost:8000/admin/
- login: admin
- password: admin
</details>

</details>

***

### Для завершения работы необходимо:

 - Нажать комбинацию клавиш `CTRL + C` в окне терминала

***

<details>
<summary>Посмотреть покрытие тестами можно:</summary>

```python
poetry run pytest
```
```python
docker-compose run --rm <имя_сервиса> pytest
например: 
docker-compose run --rm web pytest
```
Кроме того, этот проект настроен для автоматического запуска тестов с помощью GitHub Actions.
Чтобы тесты работали в GitHub Actions, вам нужно настроить секретные переменные
аналогично тем, что есть в локальном файле .env.
1. Перейдите в ваш репозиторий на GitHub.
2. Нажмите на "Settings".
3. Выберите "Secrets and variables" в меню слева.
4. Нажмите на "Actions" и добавьте каждый секрет из вашего .env файла
как новый секрет. Например, SECRET_KEY и POSTGRES_PASSWORD.

После выполнения команды push, тесты будут автоматически запущены на GitHub.
Вы можете просмотреть результаты в разделе "Actions" вашего репозитория на GitHub.
</details>

***

<details>
<summary><b>Connect with me:</b></summary>
   <p align="left">
       <a href="mailto:pafos.light@gmail.com"><img src="https://img.shields.io/badge/gmail-%23EA4335.svg?style=plastic&logo=gmail&logoColor=white" alt="Gmail"/></a>
       <a href="https://t.me/petr_lip"><img src="https://img.shields.io/badge/telegram-blue?style=plastic&logo=telegram&logoColor=white" alt="Telegram"/></a>
   </p>
</details>
