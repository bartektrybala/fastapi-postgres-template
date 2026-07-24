db:
    docker compose --file docker-compose/docker-compose-development.yaml up --remove-orphans --wait db

[working-directory('src/infrastructure/sqlalchemy')]
makemigrations:
    uv run alembic revision --autogenerate

[working-directory('src/infrastructure/sqlalchemy')]
migrate:
    uv run alembic upgrade head

run: db migrate
    uv run fastapi run --host 0.0.0.0 --port 80 src/main.py

up env="docker":
    docker compose --file docker-compose/docker-compose-{{ env }}.yaml up --build --remove-orphans --wait

down env="docker":
    docker compose --file docker-compose/docker-compose-{{ env }}.yaml down --remove-orphans

export-cue:
    cue fix
    cue export -f --out text --outfile src/env/.env.test src/env/env-test.cue
    cue export -f --out text --outfile src/env/.env.docker src/env/env-docker.cue
    cue export -f --out text --outfile src/env/.env.development src/env/env-development.cue
    cue export -f --out text --outfile src/env/.env.e2e src/env/env-e2e.cue
    cue export -f --out text --outfile api_gateway/nginx.conf api_gateway/nginx.cue
    cue export -f --out yaml --outfile docker-compose/docker-compose-docker.yaml docker-compose/docker-compose-docker.cue
    cue export -f --out yaml --outfile docker-compose/docker-compose-development.yaml docker-compose/docker-compose-development.cue
    cue export -f --out yaml --outfile docker-compose/docker-compose-e2e.yaml docker-compose/docker-compose-e2e.cue

    # PRODUCTION
    cue export -f --out text --outfile src/env/.env.production src/env/env-production.cue
    cue export -f --out text --outfile api_gateway/nginx_production.conf api_gateway/nginx_production.cue
    cue export -f --out yaml --outfile docker-compose/docker-compose-production.yaml docker-compose/docker-compose-production.cue

# ## DEV SCRIPTS ###
[working-directory('src/')]
test:
    uv run pytest

integration_test: export-cue (down "e2e") (up "e2e")
    uv run pytest -m integration

clear_cache:
    find . -type d  -name "__pycache__" -exec rm -rf {} +;
    rm -rf .pytest_cache;
    rm -rf .mypy_cache;
    rm -rf .import_linter_cache;
    rm -rf .ruff_cache;

pre-commit hook="":
    uv run pre-commit run {{ hook }} --all-files --show-diff-on-failure
