# Test database

Repository integration tests use an isolated PostgreSQL database on
`localhost:54321`.

Start it with:

```bash
docker compose -f tests/docker-compose-test.yml up -d --wait
uv run python -m pytest tests/integration
docker compose -f tests/docker-compose-test.yml down
```

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
