from __future__ import annotations

from functools import lru_cache

from pydantic import BaseSettings


class MeiliSearchConfig(BaseSettings):
    meilisearch_url: str
    meilisearch_api_key: str | None = None

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_config() -> MeiliSearchConfig:
    return MeiliSearchConfig()
