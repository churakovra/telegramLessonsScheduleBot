FROM python:3.13-slim
LABEL authors="churakovra"

WORKDIR /bot

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY app ./app

CMD ["uv","run", "python", "-m", "app.main"]