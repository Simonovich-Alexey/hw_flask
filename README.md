# Объвления

### Запуск db:
```bash
docker-compose --env-file .env_example up db -d
```
### Запуск app:
```bash
docker-compose --env-file .env_example up app -d
```

## Использование API

#### Для использования API необходимо зарегистрироваться и получить токен

### Регистрация пользователя
* **Метод**: POST
* **Endpoint**: `/user`
* **Параметры запроса**:
    - `name`: Имя пользователя
    - `email`: Email пользователя
    - `password`: Пароль пользователя

* **Пример запроса**:

```json
POST http://localhost:5000/user
Content-Type: application/json

{
  "name": "User",
  "email": "user@gmail.ru",
  "password": "password"
}
```

* **Пример ответа**:

```json
{
  "name": "User",
  "email": "user@gmail.ru",
  "password": "password"
}
```

### Получение токена
* **Метод**: POST
* **Endpoint**: `/login`
* **Параметры запроса**:
    - `name`: Имя пользователя
    - `password`: Пароль пользователя

* **Пример запроса**:

```json
POST http://localhost:5000/login
Content-Type: application/json

{
  "name": "User",
  "password": "password"
}
```

* **Пример ответа**:

```json
{
  "token": "0e4dff82-b934-4427-be45-f54ac36eafd5"
}
```

### Получение всех объявлений
* **Метод**: GET
* **Endpoint**: `/ads`

* **Пример запроса**:

```json
POST http://localhost:5000/ads
Content-Type: application/json
```

* **Пример ответа**:

```json
[
  {
    "description": "text ads",
    "id": 1,
    "owner": "User_1",
    "registration_time": "2024-03-03T12:11:29.231952",
    "title": "Title Ads"
  },
  {
    "description": "text ads 111",
    "id": 2,
    "owner": "User_1",
    "registration_time": "2024-03-03T12:11:42.437086",
    "title": "Title"
  },
  {
    "description": "text ads 111",
    "id": 3,
    "owner": "User_1",
    "registration_time": "2024-03-03T12:17:08.538390",
    "title": "Title"
  }
]
```

### Добавление объявления
* **Метод**: POST
* **Endpoint**: `/ads`
* **Параметры запроса**:
    - `title`: Заголовок объявления
    - `description`: Описание объявления

* **Пример запроса**:

```json
POST http://localhost:5000/ads
Content-Type: application/json
Authorization: 3de65cf9-e2d8-4c06-a4d8-94a38b69ae51

{
  "title": "title",
  "description": "Text"
}
```

* **Пример ответа**:

```json
{
  "description": "text ad",
  "id": 1,
  "owner": "User_1",
  "registration_time": "2024-03-03T12:17:08.538390",
  "title": "Title"
}
```

### С остальными примерами запросов вы можете ознакомится в файле `requests-examples.http`

## Завершение работы
Чтобы остановить контейнеры, выполните:
```bash
docker-compose down
```
