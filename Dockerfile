FROM python:3.14-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . /app

RUN uv sync

RUN uv run playwright install --with-deps && \
    uv run playwright install chromium

CMD  ["uv","run", "main.py"]
