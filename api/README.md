## 3. REST API Сервис

Сервис написал на [FastAPI](https://fastapi.tiangolo.com/).

- Настройки в `.env`, пример настройки в `example.env` 
    Для запуска через `docker compose` настройка бд необязательна

- Запуск через `docker`

```bash
docker compose up --build -d
```
или для сборки 
```bash
docker build -t api .
```

- Запуск напрямую

Установка зависимостей:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Запуск:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

- Тесты через `pytest`
```bash
pytest .
```
