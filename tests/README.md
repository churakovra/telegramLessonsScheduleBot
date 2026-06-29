# Test database

Tests are organized by scope and mirror the application packages:

```text
tests/
  unit/
    database/
    handlers/
    keyboard/
    message/
    middlewares/
    notifier/
    repositories/
    services/
    utils/
  integration/
    repositories/
```

Keep fast tests with mocked dependencies under `unit/`. Tests that require
PostgreSQL belong under `integration/`.

Repository integration tests use an isolated PostgreSQL database on
`localhost:54321`.

Run the complete suite:

```bash
make test
```

Run the same suite with combined unit and integration coverage:

```bash
make test-coverage
```

Both targets start PostgreSQL, run one pytest process over `tests/`, and always
stop Compose through a shell trap, including when tests fail.

Useful focused commands:

```bash
make test-unit
make test-integration
```

Pytest runs on the host through `uv`; only PostgreSQL runs in Compose. A
dedicated test-runner container is unnecessary for this project because the
locked Python environment already provides reproducible dependencies while
keeping local debugging and coverage output simpler.

The default credentials are intentionally local and disposable:

```text
database: scheduler_test
user: scheduler_test
password: scheduler_test
port: 54321
```

Override them with `TEST_DB_NAME`, `TEST_DB_USER`, `TEST_DB_PASSWORD`,
`TEST_DB_HOST`, and `TEST_DB_PORT`. `TEST_DB_NAME` must contain `test`.

The fixture creates the ORM schema at session start, truncates all tables before
each test, and drops the schema when the suite finishes.
