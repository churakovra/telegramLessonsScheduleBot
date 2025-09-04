PYTHON_VERSION := $(shell cat .python-version)
RUN := . .venv/bin/activate ;
DATABASE = scheduler-db


DATABASE_TEST = $(DATABASE)_test
EXPORT_APP_VERSION_QA = export APP_VERSION=qa;


init:
	uv venv -nv -p $(PYTHON_VERSION) .venv

install:
	$(RUN) uv sync

venv: init install

rmvenv:
	rm -rf .venv


### Start of test section ###
.PHONY: tests

export APP_VERSION=qa

tests: utests itests

utests: run_utests

utests_new: run_new_utests

utests_failed: run_failed_utests

itests: up_db_test run_test_migrations run_itests down_db_test

run_utests:
	pytest -vv tests/unit

run_new_utests:
	pytest -vv --nf tests/unit

run_failed_utests:
	pytest -vv --lf --lfnf=none tests/unit

run_itests:
	pytest -vv tests/integration

# infra for integration tests
up_db_test: down_db_test
	docker compose -f tests/docker-compose-test.yml up -d

down_db_test:
	docker compose -f tests/docker-compose-test.yml down

run_test_migrations:
	alembic upgrade head
	