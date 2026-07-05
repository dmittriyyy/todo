# 📝 Todo API

REST API для управления задачами с авторизацией пользователей.

Проект разработан на **FastAPI** с использованием **PostgreSQL**, **SQLAlchemy** и **JWT-аутентификации**. Каждый пользователь работает только со своими задачами.

---

## 🚀 Возможности

- Регистрация пользователей
- Авторизация по JWT
- Создание задач
- Получение списка своих задач
- Получение выполненных задач
- Получение задачи по ID
- Обновление информации о задаче
- Изменение статуса выполнения
- Удаление задач
- Хранение пользователей и задач в PostgreSQL

---

## 🛠 Стек технологий

- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (python-jose)
- Passlib + bcrypt
- Uvicorn
- Docker Compose

---

## 📁 Структура проекта

```
training-api/
│
├── models/             # SQLAlchemy модели
├── repository/         # Работа с базой данных
├── schemas/            # Pydantic схемы
├── utils/              # JWT и хэширование паролей
├── main.py             # Точка входа
├── bd.py               # Подключение БД
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/dmittriyyy/todo.git
cd todo
```

### 2. Создать виртуальное окружение

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

---

## 🐘 Запуск PostgreSQL

```bash
docker compose up -d
```

Будет создан контейнер:

- PostgreSQL 17
- База данных `todo_training`
- Пользователь `postgres`
- Пароль `postgres`

---

## ▶️ Запуск приложения

```bash
uvicorn main:app --reload
```

После запуска API будет доступно по адресу

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

# 🔐 Авторизация

После регистрации необходимо выполнить вход.

```
POST /auth/login
```

В ответ будет получен JWT-токен.

Для доступа к защищенным маршрутам необходимо передавать заголовок

```
Authorization: Bearer <token>
```

---

# 📚 Основные эндпоинты

## Авторизация

| Метод | Endpoint | Описание |
|--------|----------|----------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Получение JWT |

---

## Пользователь

| Метод | Endpoint | Описание |
|--------|----------|----------|
| GET | `/users/{id}` | Получение пользователя |

---

## Задачи

| Метод | Endpoint | Описание |
|--------|----------|----------|
| POST | `/tasks` | Создать задачу |
| GET | `/all_tasks` | Все задачи пользователя |
| GET | `/tasks/done` | Выполненные задачи |
| GET | `/tasks/{id}` | Получить задачу |
| PUT | `/tasks/{id}` | Полностью обновить задачу |
| PATCH | `/tasks/{id}` | Изменить статус выполнения |
| DELETE | `/tasks/{id}` | Удалить задачу |

---

## 📦 Используемые технологии

- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- JWT Authentication
- OAuth2 Password Flow
- Passlib (bcrypt)
- Docker Compose

---

## 🔒 Безопасность

- Пароли хранятся в виде bcrypt-хэшей.
- Для аутентификации используются JWT-токены.
- Каждый пользователь имеет доступ только к своим задачам.

---

## 💡 Возможности для дальнейшего развития

- Добавление сроков выполнения задач
- Категории и теги
- Приоритет задач
- Поиск и фильтрация
- Пагинация
- Unit- и Integration-тесты
- CI/CD
- Dockerfile для приложения
- Развертывание в облаке

---

## 👨‍💻 Автор

Дмитрий

GitHub: https://github.com/dmittriyyy

---

## 📄 Лицензия

Проект создан в учебных целях.
