import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass
class MeiliSearchConfig:
    url: str
    api_key: Optional[str] = None


def get_config() -> MeiliSearchConfig:
    meilisearch_url = os.getenv("MEILISEARCH_URL")
    meilisearch_api_key = os.getenv("MEILISEARCH_API_KEY")

    if not meilisearch_url:
        raise ValueError("A url for MeiliSearch is required")

    if meilisearch_api_key:
        return MeiliSearchConfig(url=meilisearch_url, api_key=meilisearch_api_key)

    return MeiliSearchConfig(url=meilisearch_url)
