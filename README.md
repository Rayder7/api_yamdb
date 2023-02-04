# Описание проекта
## api_yamdb
#### Учебный проект сайта разрабатываемая в Django_rest_framework.
#### Здесь присутствует такие возможности сайта как: 
> - Создание отзыва к произведениям
> - Создание комментариев к отзывам, авторизация с JWT
#### Все реализованно с помощью API

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/yandex-praktikum/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

# Примеры запросов к API

Получение списка произведений:
```
http://127.0.0.1:8000/api/v1/titles/
```
Список жанров:
```
http://127.0.0.1:8000/api/v1/genres/
```
Получение токена:
```
http://127.0.0.1:8000/api/v1/auth/token/
```




