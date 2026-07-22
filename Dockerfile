ARG PYTHON_VERSION=3.13
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-trixie-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    appuser

USER appuser
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src /app/src
COPY scripts /app/scripts

CMD ["uv", "run", "uvicorn", "src.main:app", "--port", "8000", "--host", "0.0.0.0"]
