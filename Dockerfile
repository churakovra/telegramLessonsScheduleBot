FROM python:3.13-slim
LABEL authors="churakovra"

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync

COPY app .

CMD ["uv", "run", "python", "-m", "app.main"]