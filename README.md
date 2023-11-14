<h1 align="center">Foodgram</h1>

Foodgram — онлайн-сервис «Продуктовый помощник».
Здесь Вы можете публиковать рецепты, подписываться на публикации других пользователей,
добавлять понравившиеся рецепты в список «Избранное»,
а перед походом в магазин скачивать сводный список продуктов,
необходимых для приготовления одного или нескольких выбранных блюд.

---
### Технологии
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

# Установка
### 1. Клонируем репозиторий
```
git clone git@github.com:ragimov700/Foodgram.git
```
### 2. Создаем .env файл
```
SECRET_KEY= # Секретный ключ Django
DEBUG= # Режим разработчики
POSTGRES_USER= # Логин БД
POSTGRES_PASSWORD= # Пароль БД
POSTGRES_DB= # Название БД
DB_HOST= # Название контейнера
DB_PORT= # Порт подключения к БД
ALLOWED_HOSTS= # Разрешенные хосты
```
### 3. Запускаем Докер в папке infra
```
sudo docker compose up -d
```
### 4. Выполняем миграции и собираем статику
```
sudo docker compose exec backend sh
python manage.py migrate
python manage.py collectstatic
```
---
<h5 align="center">Автор проекта: <a href="https://github.com/ragimov700">Sherif Ragimov</a></h5>
