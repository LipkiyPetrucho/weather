## Django-приложение, которое отображает прогноз погоды для заданного города.

### Стек технологий:

 - ![alt text](https://img.shields.io/badge/Python-3.12-grey?style=plastic&logo=python&logoColor=white&labelColor=%233776AB)

 - ![alt text](https://img.shields.io/badge/Django-5.0.7-grey?style=plastic&logo=django&logoColor=white&labelColor=%23092E20)

 - ![alt text](https://img.shields.io/badge/PostgreSQL-16.3-grey?style=plastic&logo=postgresql&logoColor=white&labelColor=%234169E1)

 - ![alt text](https://img.shields.io/badge/Docker-v25.0.3-grey?style=plastic&logo=docker&logoColor=white&labelColor=2496ED)

### Описание проекта
Разработано Django-приложение, которое отображает прогноз погоды для заданного города.

При запросе города http://localhost:8000/weather/
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
    pip install -r requirements.txt
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
    python manage.py migrate
    ```

<details>
<summary>Для создания тестового пользователя - администратор:</summary>

- login: admin@example.com
- password: admin 
    ```python
    python manage.py csu
    ```
</details>

</details>

***

### Запуск через Docker

<details>
<summary>Для запуска через Docker необходимо:</summary>

- Клонировать проект на собственный диск в новом каталоге
-  <details>
   <summary>Прописать переменные окружения в файле `.env.sample`. Имя файла необходимо заменить на .env</summary>
   
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

</details>

***

### Для завершения работы необходимо:

 - Нажать комбинацию клавиш `CTRL + C` в окне терминала

***

<details>
<summary>Посмотреть покрытие тестами можно:</summary>

```python
coverage run --source='.' manage.py test
```
```python
coverage report
```
</details>

***

<details>
<summary><b>Connect with me:</b></summary>
   <p align="left">
       <a href="mailto:pafos.light@gmail.com"><img src="https://img.shields.io/badge/gmail-%23EA4335.svg?style=plastic&logo=gmail&logoColor=white" alt="Gmail"/></a>
       <a href="https://t.me/petr_lip"><img src="https://img.shields.io/badge/telegram-blue?style=plastic&logo=telegram&logoColor=white" alt="Telegram"/></a>
   </p>
</details>
