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

up-db-test:
	docker compose -f tests/docker-compose-test.yml up -d

down-db-test:
	docker compose -f tests/docker-compose-test.yml down

.PHONY: tests

tests:
	$(EXPORT_APP_VERSION_QA) \
	pytest -vv

new-tests:
	$(EXPORT_APP_VERSION_QA) \
	$(RUN) pytest -vv --nf

failed-tests:
	$(EXPORT_APP_VERSION_QA) \
	$(RUN) pytest -vv --lf --lfnf=none