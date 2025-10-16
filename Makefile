PYTHON_VERSION := $(shell cat .python-version)
RUN := . .venv/bin/activate ;
DATABASE = scheduler-db
DB_USER = chloc
DB_HOST = localhost
DB_PORT = 5432
DB_NAME = $(DATABASE)




init:
	uv venv -nv -p $(PYTHON_VERSION) .venv

install:
	$(RUN) uv sync

venv: init install

clear:
	rm -rf .venv

create_db:
	docker exec -it postgres createdb -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) $(DB_NAME)

drop_db:
	docker exec -it postgres dropdb $(DB_NAME) -U $(DB_USER)

run_migrations:
	export DB_HOST=localhost && \
	alembic upgrade head


### Start of test section ###
DATABASE_TEST = $(DATABASE)_test
EXPORT_APP_VERSION_QA = export APP_VERSION=qa;


.PHONY: tests

tests: utests itests

utests: run_utests

utests_new: run_new_utests

utests_failed: run_failed_utests

itests: up_db_test run_test_migrations run_itests
	docker compose -f tests/docker-compose-test.yml down

run_utests:
	$(EXPORT_APP_VERSION_QA) pytest -vv tests/unit

run_new_utests:
	$(EXPORT_APP_VERSION_QA) pytest -vv --nf tests/unit

run_failed_utests:
	$(EXPORT_APP_VERSION_QA) pytest -vv --lf --lfnf=none tests/unit

run_itests:
	$(EXPORT_APP_VERSION_QA) -pytest -vv tests/integration

# infra for integration tests
up_db_test: down_db_test
	docker compose -f tests/docker-compose-test.yml up -d \
	&& sleep 1

down_db_test:
	docker compose -f tests/docker-compose-test.yml down

run_test_migrations:
	$(EXPORT_APP_VERSION_QA) alembic upgrade head
	