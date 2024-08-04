from __future__ import annotations

from meilisearch_python_sdk.models.settings import MeilisearchSettings


class MeilisearchIndexSettings(MeilisearchSettings):
    uid: str
