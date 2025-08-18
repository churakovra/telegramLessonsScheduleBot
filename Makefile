PYTHON_VERSION := $(shell cat .python-version)
RUN := . .venv/bin/activate


init:
	uv venv -nv -p $(PYTHON_VERSION) .venv

install:
	$(RUN); uv sync

venv: init install

rmvenv:
	rm -rf .venv

.PHONY: tests new-tests failed-tests

tests:
	PYTHONPATH="." pytest -vv

new-tests:
	PYTHONPATH="." pytest -vv --nf

failed-tests:
	PYTHONPATH="." pytest -vv --lf --lfnf=none