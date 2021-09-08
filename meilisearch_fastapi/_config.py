from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings


class MeiliSearchConfig(BaseSettings):
    meilisearch_url: str
    meilisearch_api_key: Optional[str] = None

    class Config:
        env_file = ".env"


@lru_cache
def get_config() -> MeiliSearchConfig:
    return MeiliSearchConfig()
