from __future__ import annotations

from async_search_client import Client
from async_search_client.models import MeiliSearchSettings, UpdateId
from fastapi import APIRouter, Depends

from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.settings import MeiliSearchIndexSettings

router = APIRouter()


@router.get("/{uid}", response_model=MeiliSearchSettings)
async def get_settings(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> MeiliSearchSettings:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.get_settings()


@router.delete("/{uid}", response_model=UpdateId)
async def delete_settings(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_settings()


@router.post("/", response_model=UpdateId)
async def update_settings(
    update_settings: MeiliSearchIndexSettings, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(update_settings.uid)

        meili_settings = MeiliSearchSettings(
            synonyms=update_settings.synonyms,
            stop_words=update_settings.stop_words,
            ranking_rules=update_settings.ranking_rules,
            attributes_for_faceting=update_settings.attributes_for_faceting,
            distinct_attribute=update_settings.distinct_attribute,
            searchable_attributes=update_settings.searchable_attributes,
            displayed_attributes=update_settings.displayed_attributes,
        )

        return await index.update_settings(meili_settings)
