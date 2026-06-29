# Testing

## Test organization

```text
tests/
├── unit/
│   ├── database/
│   ├── handlers/
│   ├── keyboard/
│   ├── message/
│   ├── middlewares/
│   ├── notifier/
│   ├── repositories/
│   ├── services/
│   └── utils/
└── integration/
    └── repositories/
```

The current suite contains 52 test functions, which expand through
parametrization to 102 collected unit test cases before integration tests.

## Unit tests

Unit tests use mocks and DTO fixtures. They cover:

- service behavior and exception translation;
- service-container wiring;
- base repository commit/flush behavior;
- unit-of-work commit and rollback;
- command handlers;
- middleware injection and transaction handling;
- keyboard generation and callback payloads;
- message serialization, formatting, producer, consumer, and direct sending;
- datetime helpers.

Run them with:

```bash
make test-unit
```

## Integration tests

Repository integration tests run against PostgreSQL 15 on
`localhost:54321`. They cover user, teacher, student, lesson, and slot
repository behavior with real SQLAlchemy statements.

The session fixture:

1. verifies database connectivity;
2. creates ORM metadata once;
3. truncates all tables before each test;
4. drops all tables after the session.

The database name must contain `test`, which protects against accidental use of
a non-test database.

Start and stop the test database manually:

```bash
make test-db-up
make test-db-down
```

Or run the integration suite with lifecycle management:

```bash
make test-integration
```

## Complete suite and coverage

```bash
make test
make test-coverage
```

Both commands start the test PostgreSQL container and stop it through a shell
trap, including after test failures. Python tests run on the host through the
locked `uv` environment.

Override test database settings with:

```text
TEST_DB_NAME
TEST_DB_USER
TEST_DB_PASSWORD
TEST_DB_HOST
TEST_DB_PORT
```

## Testing guidance

- Put pure rules and mocked collaborations in `tests/unit`.
- Use `tests/integration` when correctness depends on joins, constraints,
  ordering, transaction behavior, or PostgreSQL expressions.
- Add handler tests for user-visible responses and FSM transitions.
- Add notifier tests without a live broker by mocking channels/exchanges.
- For concurrency-sensitive booking changes, add a real PostgreSQL integration
  test with separate sessions.
