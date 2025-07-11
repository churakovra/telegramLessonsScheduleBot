FROM python:3.13-slim
LABEL authors="churakovra"

WORKDIR /bot

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app