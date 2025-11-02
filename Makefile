PYTHON_VERSION := $(shell cat .python-version)
RUN = . .venv/bin/activate;
DATABASE = scheduler-db
ENV_FILE = .env
include $(ENV_FILE)

init:
	uv venv -nv -p $(PYTHON_VERSION) .venv

install:
	$(RUN) uv sync

venv: init install

clean:
	rm -rf .venv

create_db:
	docker exec -it postgres createdb -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) $(DB_NAME)

drop_db:
	-docker exec -it postgres dropdb $(DB_NAME) -U $(DB_USER) && \
	echo 'DB $(DB_NAME) dropped successfully'

run_migrations:
	export $(APP_VERSION) && \
	$(RUN) alembic upgrade head


### Start of test section ###
DATABASE_TEST = $(DATABASE)_test
ENV_FILE_TEST = tests/.env
include $(ENV_FILE_TEST)

.PHONY: tests

tests: utests itests

utests: run_utests

utests_new: run_new_utests

utests_failed: run_failed_utests

itests: up_db_test run_test_migrations run_itests
	docker compose -f tests/docker-compose-test.yml down

run_utests:
	export $(APP_VERSION) && \
	pytest -vv tests/unit

run_new_utests:
	export $(APP_VERSION) && \
	pytest -vv --nf tests/unit

run_failed_utests:
	export $(APP_VERSION) && \
	pytest -vv --lf --lfnf=none tests/unit

run_itests:
	export $(APP_VERSION) && \
	-pytest -vv tests/integration

# infra for integration tests
up_db_test: down_db_test
	export $(POSTGRES_DB) && \
	export $(POSTGRES_USER) && \
	export $(POSTGRES_PASSWORD) && \
	docker compose -f tests/docker-compose-test.yml up -d; sleep 1

down_db_test:
	-docker compose -f tests/docker-compose-test.yml down

run_test_migrations:
	export $(APP_VERSION) && \
	$(RUN) alembic upgrade head
	