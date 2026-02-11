# Slotty 
_Version: 0.0.7_
## Возможности
### Преподаватель:
- Вносить проводимые им предметы
- Прикреплять к себе учеников - пользователей бота
- Автоматически рассылать окошки на следующую неделю всем своим ученикам
- Автоматически рассылать новостные сообщения всем своим ученикам
- Вести учёт проведенных уроков; видеть статистику по часам и доходам
### Ученик
- Получать свободные окошки от своего преподавателя(-ей)
- Записываться на урок; отменять запись
- Получать информацию о прошедших и запланированных занятиях
### Администратор
- Давать статус "Преподаватель" пользователю
- Управлять УЗ учеников и преподавателей
___
## Стек

|        Модуль        | Технология                                                         |
|:--------------------:|:-------------------------------------------------------------------|
|       **APP**        | Aiogram 3.21.0                                                     |
|        **DB**        | PostgreSQL 15<br>SQLAlchemy 2.0.41                                 |
|       **TEST**       | Pytest 8.4.1                                                       |
| **DEPLOY & <br>PROJECT** | docker<br>docker-compose<br>uv<br>alembic                      |
___
## Структура 
```
slotty/
|--app/
|  |--database/
|      |--alembic/                # Migrations
|      |--orm/                    # ORM models
|      |--database.py             # DB init
|  |--handlers/
|      |--callback                # Callback handlers
|      |--commands                # Command handlers
|      |--states                  # State handlers
|  |--keyboard/                   # Keyboard operations
|  |--middlewares/                # Middlewares
|  |--notifier/                   # Notifier service
|  |--repositories/               # DB repositories
|  |--schemas/                    # Pydantic schemas
|  |--services/                   # Services
|  |--states/                     # States initional files
|  |--utils/
|      |--config/                 # Package that contains settings.py
|      |--enums/                  # Enums
|      |--exceptions/             # Custom exceptions
|      |--bot_strings.py          # Bot strings
|      |--datetime_utils.py       # Datetime helpers
|      |--message_template.py     # Bot message templates
|  |--main.py                     # Entrypoint
|--tests/                         # Unittests
|--.env.example
|--.python-version
|--docker-compose.yml
|--Dockerfile
|--pyproject.toml
|--README.md
|--uv.lock
```
___
### Запуск
Перед запуском и клонированием проекта нужно создать собственного бота и получить `token`  
Сделать это можно по [офф. документации](https://core.telegram.org/bots/api#authorizing-your-bot)

1. Склонировать репозиторий  
```bash
git clone https://github.com/churakovra/slotty.git
```
2. Открыть и заполнить .env.example файл затем переименовать его в .env
3. Запустить сборку проекта
```bash
docker-compose up --build
```
4. \* Если докер компоуз не хочет заводиться, можно почистить кеш volume
```bash
docker-compose down -v
docker-compose up --build
```
