PYTHON_VERSION := $(shell cat .python-version)
RUN := . .venv/bin/activate


init:
	uv venv -nv -p $(PYTHON_VERSION) .venv

install:
	$(RUN); uv sync

venv: init install

rmvenv:
	rm -rf .venv

pytest:
	PYTHONPATH="." pytest . -vv