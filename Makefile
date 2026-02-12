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

lint:
	$(RUN) ruff format
	$(RUN) ruff check --fix
