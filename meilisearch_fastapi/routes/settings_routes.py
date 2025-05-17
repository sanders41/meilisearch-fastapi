from fastapi import APIRouter, Depends
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.settings import MeilisearchSettings
from meilisearch_python_sdk.models.task import TaskInfo

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi._config import MeilisearchConfig, get_config
from meilisearch_fastapi.models.settings import MeilisearchIndexSettings

router = APIRouter()


@router.get("/{uid}", response_model=MeilisearchSettings, tags=["Meilisearch Settings"])
async def get_settings(
    uid: str, client: AsyncClient = Depends(meilisearch_client)
) -> MeilisearchSettings:
    index = client.index(uid)

    return await index.get_settings()


@router.delete("/{uid}", response_model=TaskInfo, tags=["Meilisearch Settings"])
async def delete_settings(
    uid: str,
    client: AsyncClient = Depends(meilisearch_client),
    config: MeilisearchConfig = Depends(get_config),
) -> TaskInfo:
    async with AsyncClient(
        url=config.MEILISEARCH_URL, api_key=config.MEILISEARCH_API_KEY
    ) as client:
        index = client.index(uid)

        return await index.reset_settings()


@router.patch("/", response_model=TaskInfo, tags=["Meilisearch Settings"])
async def update_settings(
    update_settings: MeilisearchIndexSettings, client: AsyncClient = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(update_settings.uid)

    meili_settings = MeilisearchSettings(
        synonyms=update_settings.synonyms,
        stop_words=update_settings.stop_words,
        ranking_rules=update_settings.ranking_rules,
        filterable_attributes=update_settings.filterable_attributes,
        distinct_attribute=update_settings.distinct_attribute,
        searchable_attributes=update_settings.searchable_attributes,
        displayed_attributes=update_settings.displayed_attributes,
        sortable_attributes=update_settings.sortable_attributes,
        typo_tolerance=update_settings.typo_tolerance,
        faceting=update_settings.faceting,
        separator_tokens=update_settings.separator_tokens,
        non_separator_tokens=update_settings.non_separator_tokens,
        dictionary=update_settings.dictionary,
    )

    return await index.update_settings(meili_settings)
