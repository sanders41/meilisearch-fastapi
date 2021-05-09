from __future__ import annotations

from async_search_client import Client
from async_search_client.errors import MeiliSearchApiError
from async_search_client.models import IndexInfo, IndexStats, MeiliSearchSettings, UpdateId
from fastapi import APIRouter, Depends, HTTPException

from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.index import (
    DistinctAttribute,
    DistinctAttributeWithUID,
    IndexUpdate,
    PrimaryKey,
    RankingRules,
)
from meilisearch_fastapi.models.meili_message import MeiliSearchMessage
from meilisearch_fastapi.models.settings import MeiliSearchIndexSettings

router = APIRouter()


@router.post("/", response_model=MeiliSearchMessage)
async def create_index(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> MeiliSearchMessage:
    async with Client(config.url, api_key=config.api_key) as client:
        index = await client.create_index(uid, config.api_key)

        return MeiliSearchMessage(msg=f"Index {index.uid} created")


@router.delete("/{uid}", response_model=int)
async def delete_index(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> int:
    async with Client(config.url, api_key=config.api_key) as client:
        index = client.index(uid)
        return await index.delete()


@router.delete("/ranking-rules/{uid}", response_model=UpdateId)
async def delete_ranking_rules(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)

        return await index.reset_ranking_rules()


@router.delete("/attributes/uniquie/{uid}", response_model=UpdateId)
async def delete_distinct_attribute(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)

        return await index.reset_distinct_attribute()


@router.get("/attributes/distinct/{uid}", response_model=DistinctAttribute)
async def get_distinct_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> DistinctAttribute:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)
        attribute = await index.get_distinct_attribute()

        return DistinctAttribute(attribute=attribute)


@router.get("/{uid}", response_model=IndexInfo)
async def get_index(
    uid: str,
    config: MeiliSearchConfig = Depends(get_config),
) -> IndexInfo:
    async with Client(url=config.url, api_key=config.api_key) as client:
        # TODO: The current fetching is a hack until a decision is made as to how to best
        # handle the get_index method in the client. Once a decision is made there switch this
        # back to using the get_index from async-search-client
        # index = await client.get_index(uid)
        try:
            response = await client._http_requests.get(f"{config.url}/indexes/{uid}")

            return IndexInfo(**response.json())
        except MeiliSearchApiError as e:
            if e.status_code == 404:
                raise HTTPException(404, f"Index {uid} not found")

            raise e


@router.get("/ranking-rules/{uid}", response_model=RankingRules)
async def get_ranking_rules(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> RankingRules:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)
        ranking_rules = await index.get_ranking_rules()

        return RankingRules(ranking_rules=ranking_rules)


@router.get("/stats/{uid}", response_model=IndexStats)
async def get_stats(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> IndexStats:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)

        return await index.get_stats()


@router.get("/", response_model=list[IndexInfo])
async def get_indexes(
    config: MeiliSearchConfig = Depends(get_config),
) -> list[IndexInfo]:
    async with Client(url=config.url, api_key=config.api_key) as client:
        indexes = await client.get_indexes()

        if not indexes:
            raise HTTPException(204)

        return indexes


@router.get("/primary-key/{uid}", response_model=PrimaryKey)
async def get_primary_key(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> PrimaryKey:
    async with Client(config.url, api_key=config.api_key) as client:
        index = client.index(uid)
        primary_key = await index.get_primary_key()

        return PrimaryKey(primary_key=primary_key)


@router.put("/attributes/distinct", response_model=UpdateId)
async def update_distinct_attribute(
    attribute_with_uid: DistinctAttributeWithUID, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(config.url, api_key=config.api_key) as client:
        index = client.index(attribute_with_uid.uid)

        return await index.update_distinct_attribute(attribute_with_uid.attribute)


@router.put("/", response_model=IndexInfo)
async def update_index(
    index_update: IndexUpdate, config: MeiliSearchConfig = Depends(get_config)
) -> IndexInfo:
    async with Client(config.url, api_key=config.api_key) as client:
        # index = client.index(index_update.uid)

        # TODO: The current fetching is a hack until a decision is made as to how to best
        # handle the get_index method in the client. Once a decision is made there switch this
        # back to using the get_index from async-search-client
        # index = await client.get_index(uid)
        payload = {}
        if index_update.primary_key is not None:
            payload["primaryKey"] = index_update.primary_key
        response = await client._http_requests.put(
            f"{config.url}/indexes/{index_update.uid}", payload
        )

        return IndexInfo(**response.json())
        # return await index.update(index_update.primary_key)


@router.put("/ranking-rules", response_model=UpdateId)
async def update_ranking_rules(
    ranking_rules: MeiliSearchIndexSettings, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(ranking_rules.uid)

        ranking_rules_update = MeiliSearchSettings(
            synonyms=ranking_rules.synonyms,
            stop_words=ranking_rules.stop_words,
            ranking_rules=ranking_rules.ranking_rules,
            attributes_for_faceting=ranking_rules.attributes_for_faceting,
            distinct_attribute=ranking_rules.distinct_attribute,
            searchable_attributes=ranking_rules.searchable_attributes,
            displayed_attributes=ranking_rules.displayed_attributes,
        )

        return await index.update_ranking_rules(ranking_rules_update)
