# Slotty project documentation

Slotty is an asynchronous Telegram bot for teachers and students. Teachers
manage students, lessons, and available appointment slots; students receive
available slots and book them. An administrator can promote registered users
to teachers.

The project package is `app/`. This `docs/` directory sits beside it and
documents the behavior implemented by the current codebase (version `0.0.8`).

## Documentation map

- [Architecture](architecture.md) — runtime processes, request flow, layers,
  transactions, and package responsibilities.
- [Domain and user workflows](domain.md) — roles, entities, bot commands, and
  teacher/student flows.
- [Development](development.md) — local setup, configuration, common commands,
  migrations, and contribution guidance.
- [Operations](operations.md) — deployment topology, PostgreSQL, RabbitMQ,
  startup behavior, and operational caveats.
- [Testing](testing.md) — test layout, fixtures, commands, and coverage scope.

## Technology summary

| Area | Technology |
| --- | --- |
| Runtime | Python 3.13 (`requires-python >=3.12`) |
| Telegram framework | aiogram 3 |
| Database | PostgreSQL 15, SQLAlchemy 2 async, asyncpg |
| Validation and DTOs | Pydantic 2 |
| Messaging | RabbitMQ through aio-pika |
| Migrations | Alembic |
| Dependency management | uv |
| Tests | pytest, pytest-asyncio, pytest-cov |
| Quality | Ruff and mypy |
| Packaging/deployment | Docker and Docker Compose |

## Repository at a glance

```text
.
├── app/                    application package
│   ├── config/             environment-based settings
│   ├── database/           engine, unit of work, ORM, and migrations
│   ├── handlers/           commands, callbacks, and FSM handlers
│   ├── keyboard/           callback payloads and keyboard construction
│   ├── message/            transport-independent message models/formatters
│   ├── middlewares/        per-update dependency and transaction setup
│   ├── notifier/           RabbitMQ producer/consumer and message sender
│   ├── repositories/       SQLAlchemy persistence operations
│   ├── schemas/            Pydantic DTOs
│   ├── services/           domain/application operations
│   ├── states/             aiogram FSM definitions
│   └── utils/              strings, enums, dates, exceptions, logging
├── docs/                   project documentation
├── tests/                  unit and PostgreSQL integration tests
├── docker-compose.yml      app and notifier process definitions
├── Dockerfile              application image
├── Makefile                development command interface
├── pyproject.toml          project and tool configuration
└── uv.lock                 locked dependencies
```

## Quick start

1. Install Python 3.13, `uv`, Docker, PostgreSQL, and RabbitMQ.
2. Copy `.env.example` to `app/config/envs/dev.env` and fill in the values.
3. Install dependencies with `make install`.
4. Apply migrations with `make migrate`.
5. Run the bot with `make app`.

The local bot process still requires reachable PostgreSQL and RabbitMQ
instances. See [Development](development.md) and [Operations](operations.md)
for the complete setup and the Docker Compose limitations.

