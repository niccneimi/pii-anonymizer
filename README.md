# PII Anonymizer API

Сервис для поиска и маскирования персональных данных в тексте.

## Фичи

- **Гибридное детектирование** - комбинация Regex правил и ML-модели GLiNER
- **Fine-tuned модель** - дообучена на сгенерированных синтетических данных
- **Production-ready** - API, Docker, CI/CD пайплайн
- **Мониторинг и тесты** - покрытие тестами, логирование, метрики

## Быстрый старт

### Через Docker

```bash
docker-compose up --build
```

### Локальная разработка

```bash
pip install -r requirements.txt

uvicorn src.api.main:app --reload

pytest --cov=src
```

## API

### POST /anonymize

Маскирует персональные данные в тексте.

**Request:**
```json
{
  "text": "Меня зовут Иван, email ivan@example.com",
  "mode": "ensemble"
}
```

**Response:**
```json
{
  "anonymized_text": "Меня зовут [PERSON], email [EMAIL]"
}
```

### Компоненты

| Компонент | Описание |
|-----------|----------|
| **API** | FastAPI эндпоинт для анонимизации |
| **Regex** | Правила для email, телефонов |
| **GLiNER** | ML-модель для контекстного поиска PII |
| **Masking** | Замена найденных сущностей на токены |

## Модели

| Модель | Описание |
|--------|----------|
| **Базовая** | `urchade/gliner_medium-v2.1` — предобученная модель |
| **Fine-tuned** | Дообучена на синтетических данных с Faker |

## Метрики

| Модель | F1-Score |
|--------|----------|
| Базовая | 0.56 |
| Fine-tuned | 0.61 |
| Fine-tuned+Regex | 0.85 |

## Структура проекта

```
.
├── src/
│   ├── __init__.py
│   ├── api/          # FastAPI роуты и схемы
│   ├── detector/     # Логика детектирования PII
│   ├── monitoring/   # Логирование и метрики
│   ├── training/     # Обучение и fine-tuning
│   └── utils/        # Утилиты и хелперы
├── tests/            # Тесты
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── setup.py
```

## Требования

- Python >= 3.12
- Docker & Docker Compose
- GPU (опционально, для ускорения инференса)