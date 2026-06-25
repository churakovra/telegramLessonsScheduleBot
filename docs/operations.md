# Operations

## Container image

The Docker image:

1. starts from `python:3.13-slim`;
2. installs `uv`;
3. syncs dependencies from `pyproject.toml` and `uv.lock`;
4. copies the `app` package.

The image does not include repository-root environment files. Runtime
configuration must be supplied by the deployment or represented in the copied
`app/config/envs` directory.

## Compose services

`docker-compose.yml` defines two processes from the same image:

| Service | Mode | Command |
| --- | --- | --- |
| `scheduler` | Telegram polling and RabbitMQ producer | `uv run python -m app.main` |
| `notifier` | RabbitMQ consumer and Telegram sender | `uv run python -m app.main` with `SERVICE_TYPE=consumer` |

The scheduler publishes debugpy port `5678`.

The Compose file does **not** define PostgreSQL or RabbitMQ services. `DB_HOST`
and `AMQP_HOST` must point to externally managed services or to services added
by a deployment-specific Compose override.

## Startup dependencies

The scheduler creates the Telegram bot at import time, starts a robust RabbitMQ
producer, removes the webhook and pending updates, then begins long polling.

The notifier creates a robust RabbitMQ connection, declares the exchange and
queue, binds the queue, and waits indefinitely while consuming messages.

Database tables are not created at process startup. Apply Alembic migrations
before starting application traffic:

```bash
make migrate APP_VERSION=<environment>
```

## Message delivery

Messages published through RabbitMQ contain:

- text;
- optional parse mode;
- a transport-neutral inline keyboard;
- one or more recipient chat IDs.

The consumer acknowledges a broker message through `incoming_msg.process()`.
If validation or Telegram delivery raises an exception, aio-pika processing
semantics determine requeue/rejection behavior. There is currently no explicit
dead-letter exchange, retry policy, or per-recipient failure isolation.

## Logging and health

Application modules use `app.utils.logger.setup_logger`. There are no HTTP
health endpoints or explicit readiness checks in the application. Operational
health should currently be inferred from:

- process/container status;
- successful RabbitMQ connection logs;
- successful Telegram polling;
- PostgreSQL connectivity during handled updates;
- queue depth and consumer activity.

## Known operational caveats

- The main Compose file requires external PostgreSQL and RabbitMQ.
- `AMQP_PORT` is read but omitted from the constructed AMQP URL.
- Alembic forces the database host to `localhost`.
- Slot booking is not an atomic compare-and-set; concurrent students could
  overwrite a booking.
- The `/produce` development command targets a hard-coded chat ID.
- No database or broker startup retry/backoff is implemented beyond
  `aio_pika.connect_robust` behavior.
- The consumer sends all recipients with one `asyncio.gather`; one Telegram
  failure may fail processing of the entire envelope.
- There is no explicit graceful signal orchestration beyond `finally` blocks
  closing producer/consumer resources.
- Student menu areas and most administrator UI are incomplete.

These points describe the current implementation so deployment plans can
account for them; they are not hidden guarantees of future behavior.

## Production checklist

- Provide secrets through the deployment environment.
- Ensure `APP_VERSION` maps to the intended configuration.
- Provision PostgreSQL and RabbitMQ and verify network/DNS reachability.
- Apply migrations before starting scheduler instances.
- Run one notifier consumer at minimum.
- Restrict or disable debugpy outside development/QA.
- Remove or protect the `/produce` command.
- Add monitoring for process restarts, queue backlog, and Telegram errors.
- Back up PostgreSQL and define RabbitMQ durability/retry requirements.

