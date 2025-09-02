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

tests: up_db_test run_migrations_test run_tests down_db_test

up_db_test: down_db_test
	docker compose -f tests/docker-compose-test.yml up -d

down_db_test:
	docker compose -f tests/docker-compose-test.yml down

run_migrations_test:
	alembic upgrade head

run_tests:
	pytest -vv

new_tests:
	pytest -vv --nf

failed_tests:
	pytest -vv --lf --lfnf=none