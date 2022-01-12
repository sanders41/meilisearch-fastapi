from typing import List

from fastapi import APIRouter, Depends, HTTPException
from meilisearch_python_async import Client
from meilisearch_python_async.models.index import IndexBase, IndexInfo, IndexStats
from meilisearch_python_async.models.task import TaskId, TaskStatus

from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.index import (
    DisplayedAttributes,
    DisplayedAttributesUID,
    DistinctAttribute,
    DistinctAttributeWithUID,
    FilterableAttributes,
    FilterableAttributesWithUID,
    IndexUpdate,
    PrimaryKey,
    RankingRules,
    RankingRulesWithUID,
    SearchableAttributes,
    SearchableAttributesWithUID,
    SortableAttributes,
    SortableAttributesWithUID,
    StopWords,
    StopWordsWithUID,
    Synonyms,
    SynonymsWithUID,
)

router = APIRouter()


@router.post("/", response_model=IndexInfo, status_code=201, tags=["MeiliSearch Index"])
async def create_index(
    index_info: IndexBase, config: MeiliSearchConfig = Depends(get_config)
) -> IndexInfo:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = await client.create_index(index_info.uid, index_info.primary_key)

        return IndexInfo(
            uid=index.uid,
            primary_key=index.primary_key,
            created_at=index.created_at,
            updated_at=index.updated_at,
        )


@router.delete(
    "/filterable-attributes/{uid}",
    response_model=TaskId,
    status_code=202,
    tags=["MeiliSearch Index"],
)
async def delete_filterable_attributes(
    uid: str,
    config: MeiliSearchConfig = Depends(get_config),
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_filterable_attributes()


@router.delete(
    "/displayed-attributes/{uid}",
    response_model=TaskId,
    status_code=202,
    tags=["MeiliSearch Index"],
)
async def delete_displayed_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_displayed_attributes()


@router.delete(
    "/attributes/distinct/{uid}",
    response_model=TaskId,
    status_code=202,
    tags=["MeiliSearch Index"],
)
async def delete_distinct_attribute(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_distinct_attribute()


@router.delete("/delete-if-exists/{uid}", status_code=204, tags=["MeiliSearch Index"])
async def delete_if_exists(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> int:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        await index.delete_if_exists()
        return 204


@router.delete("/{uid}", response_model=TaskStatus, status_code=204, tags=["MeiliSearch Index"])
async def delete_index(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> TaskStatus:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        return await index.delete()


@router.delete(
    "/ranking-rules/{uid}", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def delete_ranking_rules(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_ranking_rules()


@router.delete(
    "/searchable-attributes/{uid}",
    response_model=TaskId,
    status_code=202,
    tags=["MeiliSearch Index"],
)
async def delete_searchable_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_searchable_attributes()


@router.delete(
    "/sortable-attributes/{uid}",
    response_model=TaskId,
    status_code=202,
    tags=["MeiliSearch Index"],
)
async def delete_sortable_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_sortable_attributes()


@router.delete(
    "/stop-words/{uid}", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def delete_stop_words(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_stop_words()


@router.delete(
    "/synonyms/{uid}", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def delete_synonyms(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.reset_synonyms()


@router.get(
    "/filterable-attributes/{uid}", response_model=FilterableAttributes, tags=["MeiliSearch Index"]
)
async def get_filterable_attributes(
    uid: str,
    config: MeiliSearchConfig = Depends(get_config),
) -> FilterableAttributes:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        filterable_attributes = await index.get_filterable_attributes()

        return FilterableAttributes(filterable_attributes=filterable_attributes)


@router.get(
    "/displayed-attributes/{uid}", response_model=DisplayedAttributes, tags=["MeiliSearch Index"]
)
async def get_displayed_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> DisplayedAttributes:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        displayed_attributes = await index.get_displayed_attributes()

        return DisplayedAttributes(displayed_attributes=displayed_attributes)


@router.get(
    "/attributes/distinct/{uid}", response_model=DistinctAttribute, tags=["MeiliSearch Index"]
)
async def get_distinct_attribute(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> DistinctAttribute:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        attribute = await index.get_distinct_attribute()

        return DistinctAttribute(attribute=attribute)


@router.get("/{uid}", response_model=IndexInfo, tags=["MeiliSearch Index"])
async def get_index(
    uid: str,
    config: MeiliSearchConfig = Depends(get_config),
) -> IndexInfo:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = await client.get_raw_index(uid)

        if not index:
            raise HTTPException(404, "Index not found")

        return index


@router.get("/ranking-rules/{uid}", response_model=RankingRules, tags=["MeiliSearch Index"])
async def get_ranking_rules(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> RankingRules:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        ranking_rules = await index.get_ranking_rules()

        return RankingRules(ranking_rules=ranking_rules)


@router.get("/stats/{uid}", response_model=IndexStats, tags=["MeiliSearch Index"])
async def get_stats(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> IndexStats:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.get_stats()


@router.get("/", response_model=List[IndexInfo], tags=["MeiliSearch Index"])
async def get_indexes(
    config: MeiliSearchConfig = Depends(get_config),
) -> List[IndexInfo]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        indexes = await client.get_raw_indexes()

        if not indexes:
            raise HTTPException(404, "No indexes found")

        return indexes


@router.get("/primary-key/{uid}", response_model=PrimaryKey, tags=["MeiliSearch Index"])
async def get_primary_key(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> PrimaryKey:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        primary_key = await index.get_primary_key()

        return PrimaryKey(primary_key=primary_key)


@router.get(
    "/searchable-attributes/{uid}", response_model=SearchableAttributes, tags=["MeiliSearch Index"]
)
async def get_searchable_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> SearchableAttributes:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        attributes = await index.get_searchable_attributes()

        return SearchableAttributes(searchable_attributes=attributes)


@router.get(
    "/sortable-attributes/{uid}", response_model=SortableAttributes, tags=["MeiliSearch Index"]
)
async def get_sortable_attributes(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> SortableAttributes:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        attributes = await index.get_sortable_attributes()

        return SortableAttributes(sortable_attributes=attributes)


@router.get("/stop-words/{uid}", response_model=StopWords, tags=["MeiliSearch Index"])
async def get_stop_words(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> StopWords:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        stop_words = await index.get_stop_words()

        return StopWords(stop_words=stop_words)


@router.get("/synonyms/{uid}", response_model=Synonyms, tags=["MeiliSearch Index"])
async def get_synonyms(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> Synonyms:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)
        synonyms = await index.get_synonyms()

        return Synonyms(synonyms=synonyms)


@router.put(
    "/filterable-attributes", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def update_filterable_attributes(
    filterable_attributes: FilterableAttributesWithUID,
    config: MeiliSearchConfig = Depends(get_config),
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(filterable_attributes.uid)
        attributes = filterable_attributes.filterable_attributes or []

        return await index.update_filterable_attributes(attributes)


@router.put(
    "/displayed-attributes", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def update_displayed_attributes(
    displayed_attributes: DisplayedAttributesUID, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(displayed_attributes.uid)

        return await index.update_displayed_attributes(displayed_attributes.displayed_attributes)


@router.put(
    "/attributes/distinct", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def update_distinct_attribute(
    attribute_with_uid: DistinctAttributeWithUID, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(attribute_with_uid.uid)

        return await index.update_distinct_attribute(attribute_with_uid.attribute)


@router.put("/", response_model=TaskId, tags=["MeiliSearch Index"])
async def update_index(
    index_update: IndexUpdate, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        payload = {}
        if index_update.primary_key is not None:
            payload["primaryKey"] = index_update.primary_key
        response = await client._http_requests.put(
            f"{config.meilisearch_url}/indexes/{index_update.uid}", payload
        )

        return TaskId(**response.json())


@router.put("/ranking-rules", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"])
async def update_ranking_rules(
    ranking_rules: RankingRulesWithUID, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(ranking_rules.uid)

        return await index.update_ranking_rules(ranking_rules.ranking_rules)


@router.put(
    "/searchable-attributes", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def update_searchable_attributes(
    searchable_attributes: SearchableAttributesWithUID,
    config: MeiliSearchConfig = Depends(get_config),
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(searchable_attributes.uid)

        return await index.update_searchable_attributes(searchable_attributes.searchable_attributes)


@router.put(
    "/sortable-attributes", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"]
)
async def update_sortable_attributes(
    sortable_attributes: SortableAttributesWithUID, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(sortable_attributes.uid)

        return await index.update_sortable_attributes(sortable_attributes.sortable_attributes)


@router.put("/stop-words", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"])
async def update_stop_words(
    stop_words: StopWordsWithUID, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(stop_words.uid)
        words = stop_words.stop_words or []

        return await index.update_stop_words(words)


@router.put("/synonyms", response_model=TaskId, status_code=202, tags=["MeiliSearch Index"])
async def update_synonyms(
    synonyms: SynonymsWithUID, config: MeiliSearchConfig = Depends(get_config)
) -> TaskId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(synonyms.uid)

        if not synonyms.synonyms:
            raise HTTPException(400, "No synonyms provided")

        return await index.update_synonyms(synonyms.synonyms)
