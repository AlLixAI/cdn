## Запуск проекта с использованием Docker

Чтобы запустить проект с помощью Docker, выполните команду:

```bash
docker-compose up --build
```

После сборки проект будет доступен по адресу `http://localhost:8000/`.
Визуализация графаны будет доступна по адресу `http://localhost:3000/` с логином `admin` и паролем `admin`

### Важная информация для пользователей Windows

Если вы работаете на Windows, возможно, у вас возникнут проблемы с выполнением скриптов из-за различий в стилях окончания строк между Windows (CRLF) и Linux (LF). Docker требует, чтобы файлы были в LF-формате. Это особенно важно для следующих файлов:

- `docker/start.sh`
- `docker/wait-for-it.sh`
- `docker-compose.yml`
- `Dockerfile`

Убедитесь, что указанные файлы имеют стиль строк LF. Вы можете конвертировать файлы из CRLF в LF с помощью любой текстовой редакции.


### Swagger для сервиса доступен по адресу после сборки `http://localhost:8000/docs`

### API для управления городами-узлами и поиска ближайших городов по координатам и названию.


#### 1. GET `/api/cities`
- **Описание**: Получение списка доступных городов-узлов.
- **Параметры**:
  - `limit` (опциональный, целое число >= 1): Ограничение количества возвращаемых городов.
  - `offset` (опциональный, целое число >= 0): Смещение для пагинации.
- **Ответ**: Список объектов `CityResponse`, содержащих информацию о городах.

#### 2. GET `/api/cities/{city_name}/`
- **Описание**: Получение данных по конкретному городу-узлу по названию.
- **Параметры**:
  - `city_name` (строка): Название города.
- **Ответ**: Объект `CityResponse`, содержащий информацию о городе.

#### 3. POST `/api/cities`
- **Описание**: Добавление нового города-узла.
- **Параметры**:
  - `city_name` (строка): Название города.
- **Ответ**: Объект `CityResponse`, содержащий информацию о созданном городе.

#### 4. DELETE `/api/cities/{city_name}/`
- **Описание**: Удаление города-узла.
- **Параметры**:
  - `city_name` (строка): Название города.
- **Ответ**: Нет содержимого (`204 No Content`).

#### 5. GET `/api/cities/nearest_cities_by_coord`
- **Описание**: Поиск ближайших городов-узлов по координатам.
- **Параметры**:
  - `latitude` (float): Широта.
  - `longitude` (float): Долгота.
  - `limit` (опциональный, целое число >= 1): Ограничение количества возвращаемых городов.
  - `offset` (опциональный, целое число >= 0): Смещение для пагинации.
- **Ответ**: Список объектов `CityResponse`, содержащих информацию о ближайших городах.

#### 6. GET `/api/cities/nearest_cities_by_name`
- **Описание**: Поиск ближайших городов-узлов по названию.
- **Параметры**:
  - `city_name` (строка): Название города.
  - `limit` (опциональный, целое число >= 1): Ограничение количества возвращаемых городов.
  - `offset` (опциональный, целое число >= 0): Смещение для пагинации.
- **Ответ**: Список объектов `CityResponse`, содержащих информацию о ближайших городах.
