# Описание

Веб-приложение для управления пользователями. 

### Стек

- **Python 3.13**
- **FastAPI 0.115.8**
- **Uvicorn 0.34.0**
- **SQLAlchemy 2.0.52**
- **SQLite** — база данных по умолчанию (можно заменить на PostgreSQL/MySQL)

## Структура файлов

```
anketa-app/
├── run.py                      # Точка входа FastAPI-приложения
├── config.py                   # Конфигурация (БД, отладка) из .env
├── requirements.txt            # Зависимости Python
├── .env.example                # Пример переменных окружения
├── app/
│   ├── __init__.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py           # Модель User (SQLAlchemy)
│   │   ├── services.py         # Бизнес-логика пользователей
│   │   ├── validators.py       # Валидация входных данных
│   │   ├── views.py            # Обработчики HTTP-запросов
│   │   └── urls.py             # APIRouter и маршруты /users
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py       # Обработчики ошибок
├── db/
│   ├── __init__.py
│   ├── database.py             # Инициализация БД
│   └── session.py              # Сессия SQLAlchemy
├── templates/
│   └── index.html              # Главная страница
└── static/
    ├── css/
    │   └── style.css
    └── js/
        ├── app.js              # Точка входа фронтенда
        ├── api/
            └── userApi.js      # Запросы к API пользователей

```

## Настройка и запуск

### Переменные окружения 

Создайте файл `.env` в корневой директории проекта со следующими настройками из `.env.example`:

```env
# Настройки базы данных
DATABASE_URL=sqlite:///instance/users.db

# Настройки SQLAlchemy
SQLALCHEMY_ECHO=False

# Режим отладки
DEBUG=True
```

### Создание виртуального окружения

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


#### Windows (cmd)

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt

```

### Запуск
```bash
python run.py
```

Открыть в браузере:

```
http://127.0.0.1:5000
```
## API

### POST /api/user/save — сохранить анкету

`200` - список:

```json
[
  {"id": 1, "message": "Анкета сохранена"}
]
```


### GET /api/user/all — все анкеты

`200`:

```json
[
  {
    "id": 1,
    "name": "Иван Иванов",
    "company": "ООО Компания",
    "role": "интегратор",
    "stand_interest": ["материалы о продуктах"],
    "directions": ["SmartHome"],
    "interest": ["Нужно КП"],
    "phone": "+7 988 123-45-67",
    "email": "ivan@example.com",
    "followup": "Прислать прайс",
    "created_at": "2026-09-27T10:15:00"
  }
]
```


### GET /api/user/{survey_id} — одна анкета по ID

### GET /anketa - список анкет (HTML)

### GET /anketa/export.xlsx - Excel файл со всеми анкетами




