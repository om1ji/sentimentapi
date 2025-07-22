# SentimentAPI - сервис для определения настроения текста по ключевым словам (тестовое задание)

## Запуск

1. Клонировать репозиторий (`git clone https://github.com/om1ji/sentimentapi`)

2. Создать и активировать виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установить зависимости
```bash
pip3 install -r requirements.txt
```

4. Запустить сервер
```bash
flask run --port 8000
```

## Проверка работы

### Пример POST запроса на добавление отзыва
```bash
curl -X POST http://localhost:8000/reviews \
     -H "Content-Type: application/json" \
     -d '{"text": "Это отличный сервис!"}'
```

#### Ответ
```json
{
    "created_at": "2025-07-22T17:35:42.645497",
    "id": 12,
    "sentiment": "positive",
    "text": "Это отличный сервис!"
}
```

### Пример GET запроса для получения всех отзывов (без параметров)
```bash
curl http://localhost:8000/reviews
```
#### Ответ
```json
{
    "reviews": [
        {
            "created_at": "2025-07-22T17:08:47.377412",
            "id": 1,
            "sentiment": "positive",
            "text": "Отличное заведение, уютное кафе"
        },
        {
            "created_at": "2025-07-22T17:09:09.116485",
            "id": 2,
            "sentiment": "negative",
            "text": "Мне не понравилось, плохое заведение"
        }
    ]
}
```


### Пример GET запроса с параметром по настроению
```bash
curl "http://localhost:8000/reviews?sentiment=positive"
```
#### Ответ
```json
{
    "reviews": [
        {
            "created_at": "2025-07-22T17:08:47.377412",
            "id": 1,
            "sentiment": "positive",
            "text": "Отличное заведение, уютное кафе"
        }
    ]
}
```
