@lint:
  echo black
  just --justfile {{justfile()}} black
  echo mypy
  just --justfile {{justfile()}} mypy
  echo ruff
  just --justfile {{justfile()}} ruff

@black:
  poetry run black meilisearch_fastapi tests

@mypy:
  poetry run mypy .

@ruff:
  poetry run ruff check .

@install:
  poetry install

@test: start-meilisearch-detached && stop-meilisearch
  -poetry run pytest

@start-meilisearch:
  docker compose up

@start-meilisearch-detached:
  docker compose up -d

@stop-meilisearch:
  docker compose down
