APP_VERSION ?= dev
PYTHON_VERSION := $(shell cat .python-version)

UV := uv
COMPOSE := docker compose
TEST_COMPOSE := $(COMPOSE) -f tests/docker-compose-test.yml

.DEFAULT_GOAL := help

.PHONY: help install sync check format format-check lint fix typecheck \
	test test-unit test-integration test-integration-clean test-coverage \
	test-db-up test-db-down test-db-logs \
	migrate migration \
	app app-up app-down app-logs app-config \
	clean \
	venv init run_app run_migrations test_db_up test_db_down test_integration

help:
	@printf '%s\n' \
		'Setup:' \
		'  make install                 Sync locked project dependencies' \
		'  make clean                   Remove local caches and coverage data' \
		'' \
		'Quality:' \
		'  make check                   Run format check, lint, unit tests, and compile check' \
		'  make format                  Format application and tests' \
		'  make lint                    Run Ruff without modifying files' \
		'  make fix                     Format and apply safe Ruff fixes' \
		'  make typecheck               Run mypy' \
		'' \
		'Tests:' \
		'  make test                    Run unit tests' \
		'  make test-integration        Start test DB and run integration tests' \
		'  make test-integration-clean  Run integration tests and stop test DB' \
		'  make test-coverage           Run unit tests with coverage' \
		'' \
		'Database:' \
		'  make migrate                 Upgrade the configured DB to Alembic head' \
		'  make migration MESSAGE=name  Create an Alembic migration' \
		'' \
		'Application:' \
		'  make app                     Run the bot locally' \
		'  make app-up                  Build and start app containers' \
		'  make app-down                Stop app containers' \
		'  make app-logs                Follow app container logs'

install sync:
	$(UV) sync --locked

check: format-check lint test-unit
	$(UV) run python -m compileall -q app tests

format:
	$(UV) run ruff format app tests

format-check:
	$(UV) run ruff format --check app tests

lint:
	$(UV) run ruff check app tests

fix:
	$(UV) run ruff format app tests
	$(UV) run ruff check --fix app tests

typecheck:
	$(UV) run python -m mypy app

test test-unit:
	$(UV) run python -m pytest tests/unit

test-coverage:
	$(UV) run python -m pytest tests/unit --cov=app --cov-report=term-missing

test-db-up:
	$(TEST_COMPOSE) up -d --wait

test-db-down:
	$(TEST_COMPOSE) down

test-db-logs:
	$(TEST_COMPOSE) logs -f

test-integration: test-db-up
	$(UV) run python -m pytest tests/integration

test-integration-clean:
	@set -e; \
	$(TEST_COMPOSE) up -d --wait; \
	trap '$(TEST_COMPOSE) down' EXIT; \
	$(UV) run python -m pytest tests/integration

migrate:
	APP_VERSION=$(APP_VERSION) $(UV) run python -m alembic upgrade head

migration:
	@test -n "$(MESSAGE)" || (echo "Usage: make migration MESSAGE=description" && exit 1)
	APP_VERSION=$(APP_VERSION) $(UV) run python -m alembic revision --autogenerate -m "$(MESSAGE)"

app:
	APP_VERSION=$(APP_VERSION) $(UV) run python -m app.main

app-up:
	APP_VERSION=$(APP_VERSION) $(COMPOSE) up --build -d

app-down:
	$(COMPOSE) down

app-logs:
	$(COMPOSE) logs -f scheduler notifier

app-config:
	APP_VERSION=$(APP_VERSION) $(COMPOSE) config

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache .coverage htmlcov
	find app tests -type d -name __pycache__ -prune -exec rm -rf {} +
	find app tests -type f -name '*.py[co]' -delete

# Backward-compatible aliases.
init venv: install
run_app: app-up
run_migrations: migrate
test_db_up: test-db-up
test_db_down: test-db-down
test_integration: test-integration
