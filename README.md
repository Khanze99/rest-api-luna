# Тестовое задание "Создание REST API приложения"

## Запуск через Docker Compose

### Клонируйте репозиторий
```commandline
git clone https://github.com/Khanze99/rest-api-luna.git
cd rest-api-luna
```
### Запуск 
```commandline
docker-compose up -d
```

## Документация API

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc


## Аутентификация

`X-API-Key: your-secret-api-key`


## API Endpoints
1. `GET /organizations` - список всех организаций находящихся в конкретном здании
2. `GET /organizations/in_radius/?lat=55.7558&lon=37.6173&radius_km=10` - список организаций, которые находятся в заданном радиусе/прямоугольной области относительно указанной точки на карте.
3. `GET /organizations/{id}`- вывод информации об организации по её идентификатору
4. `GET /organizations/by_activity/{activity_id}` - искать организации по виду деятельности.
5. `GET /organizations/search/?name=` - поиск организации по названию
6. `GET /organizations/by_building/{building_id}` - Организации в конкретном здании

## Переменные окружения
`DATABASE_URL=postgresql+asyncpg://luna:luna@db:5432/luna` - База данных
`API_KEY=your-secret-key-here` - API ключ


## Миграции базы данных

```commandline
docker-compose exec api uv run alembic upgrade head

docker-compose exec api uv run alembic downgrade -1
```

## Тестовые данные

Тестовые данные лежат в ./seeds/seeds.sql

Выборочно выполнить скрипт в базе данных