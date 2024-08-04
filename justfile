@lint:
  echo mypy
  just --justfile {{justfile()}} mypy
  echo ruff
  just --justfile {{justfile()}} ruff
  echo ruff-format
  just --justfile {{justfile()}} ruff-format

@mypy:
  poetry run mypy meilisearch_fastapi tests

@ruff:
  poetry run ruff check meilisearch_fastapi tests

@ruff-format:
  poetry run ruff format meilisearch_fastapi tests

@install:
  poetry install

@test:
  -poetry run pytest -x

@start-meilisearch:
  docker compose up

@start-meilisearch-detached:
  docker compose up -d

@stop-meilisearch:
  docker compose down
