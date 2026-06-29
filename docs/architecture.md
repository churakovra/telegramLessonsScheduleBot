# Architecture

## Runtime topology

The same entry point, `python -m app.main`, starts one of two service modes:

```text
Telegram updates
      |
      v
 scheduler process (SERVICE_TYPE=app)
      |                     |
      | SQL                 | MessageEnvelope JSON
      v                     v
 PostgreSQL             RabbitMQ direct exchange
                              |
                              v
                    notifier process
                              |
                              v
                       Telegram Bot API
```

- `SERVICE_TYPE=app` starts aiogram polling, the RabbitMQ producer, handlers,
  and middleware.
- `SERVICE_TYPE=consumer` starts the RabbitMQ consumer and sends queued
  messages through the Telegram bot.
- Both modes use the same bot token and configuration loader.
- In `dev` and `qa`, the app process opens debugpy on port `5678`.

Handlers that reply only to the current Telegram update may call
`message.answer` directly. Fan-out and booking notifications use
`MessageSender`, which publishes through RabbitMQ in the normal app process.

## Update processing

Each aiogram update passes through outer middleware in this order:

1. `DBSessionMiddleware` opens an async SQLAlchemy session and creates a
   `UnitOfWork`.
2. `ServicesMiddleware` builds the `Services` container from unit-of-work
   repositories.
3. `UserMiddleware` looks up the Telegram username and injects a `UserDTO`
   when the user is registered.
4. `SenderInjectionMiddleware` injects the dispatcher `MessageSender`, with a
   direct-bot fallback for contexts without a producer.
5. The matching command, callback, or FSM handler runs.
6. The unit of work commits after success or rolls back after an exception.

This gives one database transaction per Telegram update. Repositories created
by `UnitOfWork` set `auto_commit=False`, so individual repository methods flush
changes but leave the transaction boundary to middleware.

## Application layers

```text
handlers / middlewares
          |
          v
       services
          |
          v
     repositories
          |
          v
 SQLAlchemy ORM + PostgreSQL
```

### Handlers

`app/handlers` contains:

- commands: `/start`, `/menu`, `/cancel`, `/make_teacher`, and `/produce`;
- callbacks grouped into common, teacher, and student behavior;
- FSM handlers for multi-message lesson, student, and slot workflows.

Routers are collected in `app.handlers.register_routers`.

### Services

Services contain application rules and translate missing data into domain
exceptions. `Services` exposes:

- `user` — registration, role changes, user lookup and display;
- `teacher` — teacher lookup and teacher/student relationships;
- `student` — student lookup, parsing usernames, and teacher-scoped lists;
- `slot` — slot parsing, synchronization, lookup, booking, and deletion;
- `lesson` — lesson CRUD and teacher/student lesson assignments.

Each service accepts either an async session or a repository, which keeps unit
tests independent from PostgreSQL.

### Repositories

Repositories own SQLAlchemy statements and DTO conversion. `BaseRepository`
provides shared add, bulk-add, update/delete execution, scalar lookup, and DTO
helpers.

Repository methods normally auto-commit when created directly. Repositories
inside `UnitOfWork` disable auto-commit and participate in the middleware
transaction.

### Schemas and ORM

SQLAlchemy ORM models represent persisted entities. Pydantic DTOs are used
across service and handler boundaries. Create/update DTOs validate incoming
application data before it reaches the repositories.

Slot DTOs normalize timestamps to UTC+3 for presentation and application use.
Database columns use timezone-aware timestamps.

## Telegram UI model

Inline keyboards are represented by transport-independent Pydantic models:

- `BotMessage`
- `MarkupData`
- `RowData`
- `ButtonData`

`app.keyboard.fabric` creates these models, and `BotMessage.to_aiogram_kwargs`
converts them to aiogram objects only at the delivery boundary. Callback data
classes provide compact, typed payloads for menu and entity operations.

## Notification model

`MessageSender` provides one interface with two transports:

- a `MessageProducer`, which publishes a serialized `MessageEnvelope`;
- an aiogram `Bot`, which sends directly when no producer is configured.

The producer declares the configured direct exchange and publishes using one
routing key. The consumer declares and binds the queue, validates JSON with
Pydantic, reconstructs aiogram arguments, and sends to all recipients
concurrently.

Current broker constants:

| Setting | Value |
| --- | --- |
| Exchange | `slotty` |
| Exchange type | `direct` |
| Queue | `slotty_messages` |
| Routing key | `slotty_message` |

## Package responsibility guide

| Package | Put code here when it… |
| --- | --- |
| `handlers` | reacts to Telegram events or advances an FSM |
| `keyboard` | defines callback payloads or builds inline keyboard data |
| `message` | models or formats outgoing messages |
| `middlewares` | supplies cross-cutting update context |
| `services` | expresses application rules or coordinates repositories |
| `repositories` | reads or writes persistent data |
| `schemas` | defines validated data passed between layers |
| `database/orm` | defines persisted tables and relationships |
| `notifier` | transports messages outside the current update |
| `utils` | contains small shared constants/helpers without domain ownership |

