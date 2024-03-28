
# Сервис поиска ближайших машин для перевозки грузов
___

### стек

+ python3.11 <img height="24" width="24" src="https://cdn.simpleicons.org/python/5066b3" />
+ Django 5.0.3 <img height="24" width="24" src="https://cdn.simpleicons.org/django/5066b3" />
+ Postgres 15.0 <img height="24" width="24" src="https://cdn.simpleicons.org/postgresql/5066b3" />
+ Docker <img height="24" width="24" src="https://cdn.simpleicons.org/docker/5066b3" />
+ poetry<img height="24" width="24" src="https://cdn.simpleicons.org/poetry/" />
+ nginx <img height="24" width="24" src="https://cdn.simpleicons.org/nginx/5066b3" />
+ Celery <img height="24" width="24" src="https://cdn.simpleicons.org/celery/5066b3" />
+ pytest <img height="24" width="24" src="https://cdn.simpleicons.org/pytest/5066b3" />
+ gunicorn <img height="24" width="24" src="https://cdn.simpleicons.org/gunicorn/5066b3" />
+ pre-commit 3.7.0
+ DRF 3.15.1
+ Docker-compose

В данном проекте реализован поиск ближайших машин к грузу на Django с использованием DRF.
Список не обходимых переменных окружения находится в .env_example


## Установка:
1. Клонируйте репозиторий с github на локальный компьютер
2. Создайте виртуальное окружение
3. установите poetry командой `pip install poetry`
4. проинициализируйте poetry командой `poetry init`
5. установите зависимости командой `poetry install`
6. Создайте в корне проекта файл в .env и .env_docker и заполните переменными окружения из .env_example
7. Соберите и поднимите docker-контейнер командой `docker-compose up -d --build`
8. Для запуска тестов запустите сервер командой `python3 manage.py runserver` и выполните команду `pytest`
9. 


## Список приложений проекта и их реализация:
+ ### car
  + [x] Обновление информации о машине
- ### cargo
    + [x] Создание нового груза
    + [x] Изменение информации о грузе
    + [x] Получение списка грузов со списком машин в радиусе 450 миль
    + [x] Получение груза по id и информации о всех машинах (номер и расстояние до выбранного груза) 
    + [x] Удаление груза


- ### SWAGGER: http://localhost:8000/docs/swagger

