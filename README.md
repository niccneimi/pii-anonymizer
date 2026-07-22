# PII Anonymizer API

Сервис для поиска и маскирования персональных данных в тексте.

## Фичи

- **Гибридное детектирование** - комбинация Regex правил и ML-модели GLiNER
- **Fine-tuned модель** - дообучена на сгенерированных синтетических данных
- **Production-ready** - API, Docker, CI/CD пайплайн
- **Мониторинг** - полный стек: Prometheus, Loki, Grafana, Promtail
- **Автоматический деплой** - CI/CD через GitHub Actions на VDS
- **Тесты и качество** - покрытие тестами, логирование, метрики

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

---

## 📊 Мониторинг и Observability

Сервис оснащен полным стеком мониторинга для отслеживания состояния, производительности и логирования.

### Стек мониторинга

| Компонент | Назначение |
|-----------|------------|
| **Prometheus** | Сбор метрик с приложения |
| **Loki** | Агрегация и хранение логов |
| **Promtail** | Сбор и отправка логов в Loki |
| **Grafana** | Визуализация дашбордов и алертинг |

### Доступные метрики

- **HTTP-метрики**: статусы ответов, время обработки запросов
- **Системные метрики**: использование CPU, RAM, дисковое пространство

### Дашборды Grafana

В Grafana настроены следующие дашборды:
- **Общий статус**: количество запросов, ошибок, время ответа, rps
- **Логи**: поиск и фильтрация логов через Loki

### Запуск стека мониторинга

После запуска:
- Grafana: `http://localhost:3000` (admin/admin)
- Prometheus: `http://localhost:9090`
- Loki: `http://localhost:3100`
- Promtail: `http://localhost:9080`

---

## 🚀 Деплой и CI/CD

### Автоматический деплой на сервер

Настроен полноценный CI/CD пайплайн через GitHub Actions

### Переменные окружения для CI/CD

Для работы деплоя в GitHub Actions настроены следующие secrets:

| Secret | Назначение |
|--------|------------|
| `SERVER_IP` | IP-адрес сервера |
| `SERVER_USER` | Пользователь для SSH |
| `SSH_PRIVATE_KEY` | Приватный ключ для подключения |

### Ручной деплой

Если нужно запустить деплой вручную:

```bash
ssh user@your-server-ip

cd /home/pii-anonymizer

git pull origin main
docker compose up -d --build
```

---

## Структура проекта

```
.
├── .github/
│   └── workflows/        # CI/CD пайплайны
│       └── ci.yml
├── src/
│   ├── __init__.py
│   ├── api/              # FastAPI роуты и схемы
│   ├── detector/         # Логика детектирования PII
│   ├── monitoring/       # Логирование и метрики
│   ├── training/         # Обучение и fine-tuning
│   └── utils/            # Утилиты и хелперы
├── tests/                # Тесты
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── setup.py
```

## Требования

- Python >= 3.12
- Docker & Docker Compose
- GPU (опционально, для ускорения инференса)