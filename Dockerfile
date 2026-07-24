ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-trixie-slim AS builder

RUN apt update && apt install -y libpq-dev gcc

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:${PYTHON_VERSION}-slim-trixie AS runner
RUN apt update && apt install -y libpq5

RUN adduser --disabled-password --shell "/sbin/nologin" appuser
USER appuser
WORKDIR /app

COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --chown=appuser:appuser src /app/src

ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
