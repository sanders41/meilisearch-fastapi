from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from meilisearch_python_async import Client
from meilisearch_python_async.models.index import IndexBase, IndexInfo, IndexStats
from meilisearch_python_async.models.settings import Faceting
from meilisearch_python_async.models.task import TaskInfo

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.index import (
    DisplayedAttributes,
    DisplayedAttributesUID,
    DistinctAttribute,
    DistinctAttributeWithUID,
    FacetingWithUID,
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
    TypoTolerance,
    TypoToleranceWithUID,
)

router = APIRouter()


@router.post("/", response_model=IndexInfo, status_code=201, tags=["Meilisearch Index"])
async def create_index(
    index_info: IndexBase, client: Client = Depends(meilisearch_client)
) -> IndexInfo:
    index = await client.create_index(index_info.uid, index_info.primary_key)

    return IndexInfo(
        uid=index.uid,
        primary_key=index.primary_key,
        created_at=index.created_at,
        updated_at=index.updated_at,
    )


@router.delete("/faceting/{uid}", response_model=TaskInfo, tags=["Meilisearch Index"])
async def delete_faceting(uid: str, client: Client = Depends(meilisearch_client)) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_faceting()


@router.delete(
    "/filterable-attributes/{uid}",
    response_model=TaskInfo,
    status_code=202,
    tags=["Meilisearch Index"],
)
async def delete_filterable_attributes(
    uid: str,
    client: Client = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_filterable_attributes()


@router.delete(
    "/displayed-attributes/{uid}",
    response_model=TaskInfo,
    status_code=202,
    tags=["Meilisearch Index"],
)
async def delete_displayed_attributes(
    uid: str, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_displayed_attributes()


@router.delete(
    "/attributes/distinct/{uid}",
    response_model=TaskInfo,
    status_code=202,
    tags=["Meilisearch Index"],
)
async def delete_distinct_attribute(
    uid: str, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_distinct_attribute()


@router.delete("/delete-if-exists/{uid}", status_code=204, tags=["Meilisearch Index"])
async def delete_if_exists(uid: str, client: Client = Depends(meilisearch_client)) -> int:
    index = client.index(uid)
    await index.delete_if_exists()
    return status.HTTP_204_NO_CONTENT


@router.delete("/{uid}", response_model=TaskInfo, tags=["Meilisearch Index"])
async def delete_index(uid: str, client: Client = Depends(meilisearch_client)) -> TaskInfo:
    index = client.index(uid)
    return await index.delete()


@router.delete(
    "/ranking-rules/{uid}", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def delete_ranking_rules(uid: str, client: Client = Depends(meilisearch_client)) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_ranking_rules()


@router.delete(
    "/searchable-attributes/{uid}",
    response_model=TaskInfo,
    status_code=202,
    tags=["Meilisearch Index"],
)
async def delete_searchable_attributes(
    uid: str, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_searchable_attributes()


@router.delete(
    "/sortable-attributes/{uid}",
    response_model=TaskInfo,
    status_code=202,
    tags=["Meilisearch Index"],
)
async def delete_sortable_attributes(
    uid: str, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_sortable_attributes()


@router.delete(
    "/stop-words/{uid}", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def delete_stop_words(uid: str, client: Client = Depends(meilisearch_client)) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_stop_words()


@router.delete(
    "/synonyms/{uid}", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def delete_synonyms(uid: str, client: Client = Depends(meilisearch_client)) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_synonyms()


@router.delete(
    "/typo-tolerance/{uid}", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def delete_typo_tolerance(uid: str, client: Client = Depends(meilisearch_client)) -> TaskInfo:
    index = client.index(uid)

    return await index.reset_typo_tolerance()


@router.get("/faceting/{uid}", response_model=Faceting, tags=["Meilisearch Index"])
async def get_faceting(uid: str, client: Client = Depends(meilisearch_client)) -> Faceting:
    index = client.index(uid)
    faceting = await index.get_faceting()

    return faceting


@router.get(
    "/filterable-attributes/{uid}", response_model=FilterableAttributes, tags=["Meilisearch Index"]
)
async def get_filterable_attributes(
    uid: str,
    client: Client = Depends(meilisearch_client),
) -> FilterableAttributes:
    index = client.index(uid)
    filterable_attributes = await index.get_filterable_attributes()

    return FilterableAttributes(filterable_attributes=filterable_attributes)


@router.get(
    "/displayed-attributes/{uid}", response_model=DisplayedAttributes, tags=["Meilisearch Index"]
)
async def get_displayed_attributes(
    uid: str, client: Client = Depends(meilisearch_client)
) -> DisplayedAttributes:
    index = client.index(uid)
    displayed_attributes = await index.get_displayed_attributes()

    return DisplayedAttributes(displayed_attributes=displayed_attributes)


@router.get(
    "/attributes/distinct/{uid}", response_model=DistinctAttribute, tags=["Meilisearch Index"]
)
async def get_distinct_attribute(
    uid: str, client: Client = Depends(meilisearch_client)
) -> DistinctAttribute:
    index = client.index(uid)
    attribute = await index.get_distinct_attribute()

    return DistinctAttribute(attribute=attribute)


@router.get("/{uid}", response_model=IndexInfo, tags=["Meilisearch Index"])
async def get_index(
    uid: str,
    client: Client = Depends(meilisearch_client),
) -> IndexInfo:
    index = await client.get_raw_index(uid)

    if not index:
        raise HTTPException(404, "Index not found")

    return index


@router.get("/ranking-rules/{uid}", response_model=RankingRules, tags=["Meilisearch Index"])
async def get_ranking_rules(uid: str, client: Client = Depends(meilisearch_client)) -> RankingRules:
    index = client.index(uid)
    ranking_rules = await index.get_ranking_rules()

    return RankingRules(ranking_rules=ranking_rules)


@router.get("/stats/{uid}", response_model=IndexStats, tags=["Meilisearch Index"])
async def get_stats(uid: str, client: Client = Depends(meilisearch_client)) -> IndexStats:
    index = client.index(uid)

    return await index.get_stats()


@router.get("/", response_model=List[IndexInfo], tags=["Meilisearch Index"])
async def get_indexes(
    client: Client = Depends(meilisearch_client),
) -> List[IndexInfo]:
    indexes = await client.get_raw_indexes()

    if not indexes:
        raise HTTPException(404, "No indexes found")

    return indexes


@router.get("/primary-key/{uid}", response_model=PrimaryKey, tags=["Meilisearch Index"])
async def get_primary_key(uid: str, client: Client = Depends(meilisearch_client)) -> PrimaryKey:
    index = client.index(uid)
    primary_key = await index.get_primary_key()

    return PrimaryKey(primary_key=primary_key)


@router.get(
    "/searchable-attributes/{uid}", response_model=SearchableAttributes, tags=["Meilisearch Index"]
)
async def get_searchable_attributes(
    uid: str, client: Client = Depends(meilisearch_client)
) -> SearchableAttributes:
    index = client.index(uid)
    attributes = await index.get_searchable_attributes()

    return SearchableAttributes(searchable_attributes=attributes)


@router.get(
    "/sortable-attributes/{uid}", response_model=SortableAttributes, tags=["Meilisearch Index"]
)
async def get_sortable_attributes(
    uid: str, client: Client = Depends(meilisearch_client)
) -> SortableAttributes:
    index = client.index(uid)
    attributes = await index.get_sortable_attributes()

    return SortableAttributes(sortable_attributes=attributes)


@router.get("/stop-words/{uid}", response_model=StopWords, tags=["Meilisearch Index"])
async def get_stop_words(uid: str, client: Client = Depends(meilisearch_client)) -> StopWords:
    index = client.index(uid)
    stop_words = await index.get_stop_words()

    return StopWords(stop_words=stop_words)


@router.get("/synonyms/{uid}", response_model=Synonyms, tags=["Meilisearch Index"])
async def get_synonyms(uid: str, client: Client = Depends(meilisearch_client)) -> Synonyms:
    index = client.index(uid)
    synonyms = await index.get_synonyms()

    return Synonyms(synonyms=synonyms)


@router.get("/typo-tolerance/{uid}", response_model=TypoTolerance, tags=["Meilisearch Index"])
async def get_typo_tolerance(
    uid: str, client: Client = Depends(meilisearch_client)
) -> TypoTolerance:
    index = client.index(uid)
    typo_tolerance = await index.get_typo_tolerance()

    return TypoTolerance(typo_tolerance=typo_tolerance)


@router.patch("/faceting", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"])
async def update_faceting(
    faceting: FacetingWithUID,
    client: Client = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(faceting.uid)

    return await index.update_faceting(Faceting(max_values_per_facet=faceting.max_values_per_facet))


@router.patch(
    "/filterable-attributes", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_filterable_attributes(
    filterable_attributes: FilterableAttributesWithUID,
    client: Client = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(filterable_attributes.uid)
    attributes = filterable_attributes.filterable_attributes or []

    return await index.update_filterable_attributes(attributes)


@router.patch(
    "/displayed-attributes", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_displayed_attributes(
    displayed_attributes: DisplayedAttributesUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(displayed_attributes.uid)

    return await index.update_displayed_attributes(displayed_attributes.displayed_attributes)


@router.patch(
    "/attributes/distinct", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_distinct_attribute(
    attribute_with_uid: DistinctAttributeWithUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(attribute_with_uid.uid)

    return await index.update_distinct_attribute(attribute_with_uid.attribute)


@router.patch("/", response_model=TaskInfo, tags=["Meilisearch Index"])
async def update_index(
    index_update: IndexUpdate,
    client: Client = Depends(meilisearch_client),
    config: MeiliSearchConfig = Depends(get_config),
) -> TaskInfo:
    payload = {}
    if index_update.primary_key is not None:
        payload["primaryKey"] = index_update.primary_key
    response = await client._http_requests.patch(
        f"{config.meilisearch_url}/indexes/{index_update.uid}", payload
    )

    return TaskInfo(**response.json())


@router.patch(
    "/ranking-rules", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_ranking_rules(
    ranking_rules: RankingRulesWithUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(ranking_rules.uid)

    return await index.update_ranking_rules(ranking_rules.ranking_rules)


@router.patch(
    "/searchable-attributes", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_searchable_attributes(
    searchable_attributes: SearchableAttributesWithUID,
    client: Client = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(searchable_attributes.uid)

    return await index.update_searchable_attributes(searchable_attributes.searchable_attributes)


@router.patch(
    "/sortable-attributes", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_sortable_attributes(
    sortable_attributes: SortableAttributesWithUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(sortable_attributes.uid)

    return await index.update_sortable_attributes(sortable_attributes.sortable_attributes)


@router.patch("/stop-words", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"])
async def update_stop_words(
    stop_words: StopWordsWithUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(stop_words.uid)
    words = stop_words.stop_words or []

    return await index.update_stop_words(words)


@router.patch("/synonyms", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"])
async def update_synonyms(
    synonyms: SynonymsWithUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(synonyms.uid)

    if not synonyms.synonyms:
        raise HTTPException(400, "No synonyms provided")

    return await index.update_synonyms(synonyms.synonyms)


@router.patch(
    "/typo-tolerance", response_model=TaskInfo, status_code=202, tags=["Meilisearch Index"]
)
async def update_typo_tolerance(
    typo_tolerance: TypoToleranceWithUID, client: Client = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(typo_tolerance.uid)

    if not typo_tolerance.typo_tolerance:
        raise HTTPException(400, "No typo tolerance provided")

    return await index.update_typo_tolerance(typo_tolerance.typo_tolerance)
