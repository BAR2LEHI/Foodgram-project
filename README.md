Сайт доступен по адресу - http://158.160.28.68:8080
Username суперпользователя - vladtarasov
Password суперпользователя - dkflnfhfcjd2001
# Foodgram
### Описание

##### API проекта Foodgram.

Проект Foodgram позволяет пользователям публиковать их собственные(необязательно) рецепты блюд, добавлять их в избранное, а так же в список покупок.  
Пользователи могут подписываться на других авторов и следить за их новыми кулинарными шедеврами.  
Присутствует возможность скачать csv файл с необходимым количеством ингредиентов для приготовления всех рецептов, которые были добавлены пользователем в свой список покупок.

### Технологии
* Python 3.9
* Django 3.2
* djangorestframework 3.12.4
### Как запустить проект:

Клонировать репозиторий:

```
git clone git@github.com:BAR2LEHI/foodgram-project-react.git
```
 Перейти в папку с данным проектом: 
```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас Windows

    ```
    source venv/Scripts/activate
    ```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

```
cd foodgram-project-react
```

Выполнить миграции:

```
python manage.py migrate
```

Заполните базу данных ингредиентами из csv-файла. 

```
python manage.py add_ingredients
```

Запустить проект:

```
python manage.py runserver
```

Документация к API подключена по адресу:

```
http://127.0.0.1:8000/redoc/
```

## Примеры работы некоторых эндпоинтов проекта:

### 1) Регистрация пользователей и выдача токенов

#### Регистрация нового пользователя

Права доступа - всем пользователям.  
Поля email и username должны быть уникальны.
```
POST http://127.0.0.1:8000/api/users/
```
Пример запроса:
```
{
  "email": "vpupkin@yandex.ru",
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Qwerty123"
}
```
Пример ответа:
```
{
  "email": "vpupkin@yandex.ru",
  "id": 0,
  "username": "vasya.pupkin",
  "first_name": "Вася",
  "last_name": "Пупкин"
}
```

#### Получение токена (авторизация)
Права доступа - всем пользователям.  
Обязательные поля: email, password.
```
POST http://127.0.0.1:8000/api/auth/token/login/
```
Пример запроса:
```
{
  "password": "string",
  "email": "string"
}
```
Пример ответа:
```
{
  "auth_token": "string"
}
```

### 2) Рецепты
#### Список рецептов
Права доступа - всем пользователям.  
Доступна фильтрация по избранному, автору, списку покупок и тегам. 
```
GET http://127.0.0.1:8000/api/recipes/
```
Принимаемые параметры:
```
page - integer (номер страницы)
limit - integer (количество обьектов на странице)
is_favorited - integer: 1 либо 0 (показывать только рецепты, находящиеся в списке избранного)
is_in_shopping_cart - integer: 1 либо 0 (показывать только рецепты, находящиеся в списке покупок)
author - integer (показывать рецепты только автора с указанным id)
tags = array of strings(показывать рецепты только с указанными тегами (по slug))  
```
Пример ответа:
```
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorited": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

#### Создание рецепта
Права доступа - авторизованным пользователям.  
Обязательные поля: tags, ingredients, name, image, text, cooking_time.
```
POST http://127.0.0.1:8000/api/recipes/
```
Пример запроса:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

#### Получение рецепта
Права доступа - всем пользователям.  
Принимаемый аргумент - id (Уникальный идентификатор этого рецепта).
```
GET http://127.0.0.1:8000/api/recipes/1/
```
Пример ответа:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```
#### Обновление рецепта
Права доступа - только автор данного рецепта.  
Необходимо обратить внимание, что нужно передать все поля, так как задействован метод PATCH.
```
PATCH http://127.0.0.1:8000/api/recipes/1/
```
Пример запроса:
```
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
Пример ответа:
```
{
  "id": 0,
  "tags": [
    {
      "id": 0,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    }
  ],
  "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 0,
      "name": "Картофель отварной",
      "measurement_unit": "г",
      "amount": 1
    }
  ],
  "is_favorited": true,
  "is_in_shopping_cart": true,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "string",
  "cooking_time": 1
}
```

#### Удаление рецепта
Права доступа - только автору данного рецепта.  
Принимаемый аргумент - id (Уникальный идентификатор этого рецепта)
```
DELETE http://127.0.0.1:8000/api/recipes/1/
```
Пример ответа:
```
HTTP Status 204
```

@Foodgram   
Author Vladislav Tarasov.