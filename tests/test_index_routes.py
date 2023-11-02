from uuid import uuid4

import pytest
from meilisearch_python_async.models.settings import MeilisearchSettings
from meilisearch_python_async.task import wait_for_task


@pytest.fixture
def new_settings():
    return MeilisearchSettings(
        ranking_rules=["typo", "words"], searchable_attributes=["title", "overview"]
    )


@pytest.fixture
def default_ranking_rules():
    return ["words", "typo", "proximity", "attribute", "sort", "exactness"]


@pytest.fixture
def new_ranking_rules():
    return ["typo", "exactness"]


@pytest.fixture
def new_distinct_attribute():
    return "title"


@pytest.fixture
def default_distinct_attribute():
    return None


@pytest.fixture
def new_searchable_attributes():
    return ["something", "random"]


@pytest.fixture
def displayed_attributes():
    return ["id", "release_date", "title", "poster", "overview", "genre"]


@pytest.fixture
def new_stop_words():
    return ["of", "the"]


@pytest.fixture
def new_synonyms():
    return {"hp": ["harry potter"]}


@pytest.fixture
def new_typo_tolerance():
    return {
        "enabled": False,
        "disableOnAttributes": ["title"],
        "disableOnWords": ["spiderman"],
        "minWordSizeForTypos": {
            "oneTypo": 10,
            "twoTypos": 20,
        },
    }


@pytest.fixture
def faceting():
    return 90


@pytest.fixture
def filterable_attributes():
    return ["release_date", "title"]


@pytest.fixture
def sortable_attributes():
    return ["genre", "title"]


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {
                "uid": "test",
                "primaryKey": "pk",
            },
            {
                "uid": "test",
                "primary_key": "pk",
            },
        ),
        (
            {
                "uid": "test",
            },
            {
                "uid": "test",
                "primary_key": None,
            },
        ),
    ],
)
async def test_create_index(fastapi_test_client, data, expected):
    index = await fastapi_test_client.post("/indexes", json=data)

    assert index.json()["uid"] == expected["uid"]
    assert index.json()["primaryKey"] == expected["primary_key"]
    assert "createdAt" in index.json()
    assert "updatedAt" in index.json()


@pytest.mark.usefixtures("indexes_sample")
async def test_get_index(fastapi_test_client, index_uid):
    response = await fastapi_test_client.get(f"/indexes/{index_uid}")
    assert response.json()["uid"] == index_uid


async def test_get_index_none(fastapi_test_client):
    response = await fastapi_test_client.get("/indexes/bad")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
async def test_get_indexes(fastapi_test_client, index_uid, index_uid2):
    response = await fastapi_test_client.get("/indexes")
    response_uids = [x["uid"] for x in response.json()]

    assert index_uid in response_uids
    assert index_uid2 in response_uids
    assert len(response.json()) == 2


async def test_get_indexes_none(fastapi_test_client):
    response = await fastapi_test_client.get("/indexes")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
async def test_get_primary_key(fastapi_test_client, index_uid2):
    response = await fastapi_test_client.get(f"/indexes/primary-key/{index_uid2}")
    assert response.json()["primaryKey"] == "book_id"


@pytest.mark.usefixtures("indexes_sample")
async def test_delete_index(fastapi_test_client, index_uid, index_uid2, async_client):
    response = await fastapi_test_client.delete(f"indexes/{index_uid}")
    await wait_for_task(async_client.http_client, response.json()["taskUid"])

    response = await fastapi_test_client.get(f"/indexes/{index_uid}")
    assert response.status_code == 404

    response = await fastapi_test_client.delete(f"indexes/{index_uid2}")
    await wait_for_task(async_client.http_client, response.json()["taskUid"])

    response = await fastapi_test_client.get(f"/indexes/{index_uid2}")
    assert response.status_code == 404

    response = await fastapi_test_client.get("/indexes")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
@pytest.mark.parametrize("test_uid", ["indexUID", "none"])
async def test_delete_if_exists(fastapi_test_client, test_uid):
    response = await fastapi_test_client.delete(f"/indexes/delete-if-exists/{test_uid}")
    assert response.status_code == 204

    response = await fastapi_test_client.get(f"/indexes/{test_uid}")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
async def test_update_index(fastapi_test_client, index_uid, async_client):
    primay_key = "objectID"
    update_data = {"uid": index_uid, "primaryKey": primay_key}
    update = await fastapi_test_client.patch("/indexes", json=update_data)
    await wait_for_task(async_client.http_client, update.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/{index_uid}")
    response_primary_key = response.json()["primaryKey"]

    assert response_primary_key == primay_key


async def test_get_stats(fastapi_test_client, async_empty_index, small_movies):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "documents": small_movies}
    update = await fastapi_test_client.put("/documents", json=data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/stats/{uid}")

    assert response.json()["numberOfDocuments"] == 30


async def test_get_ranking_rules_default(
    fastapi_test_client, async_empty_index, default_ranking_rules
):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == default_ranking_rules


async def test_update_ranking_rules(fastapi_test_client, async_empty_index, new_ranking_rules):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "rankingRules": new_ranking_rules}
    response = await fastapi_test_client.patch("/indexes/ranking-rules", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == new_ranking_rules


async def test_reset_ranking_rules(
    fastapi_test_client, async_empty_index, new_ranking_rules, default_ranking_rules
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "rankingRules": new_ranking_rules}
    response = await fastapi_test_client.patch("/indexes/ranking-rules", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == new_ranking_rules
    response = await fastapi_test_client.delete(f"/indexes/ranking-rules/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == default_ranking_rules


async def test_get_distinct_attribute(
    fastapi_test_client, async_empty_index, default_distinct_attribute
):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == default_distinct_attribute


async def test_update_distinct_attribute(
    fastapi_test_client, async_empty_index, new_distinct_attribute
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "attribute": new_distinct_attribute}
    response = await fastapi_test_client.patch("/indexes/attributes/distinct", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == new_distinct_attribute


async def test_reset_distinct_attribute(
    fastapi_test_client, async_empty_index, new_distinct_attribute, default_distinct_attribute
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "attribute": new_distinct_attribute}
    response = await fastapi_test_client.patch("/indexes/attributes/distinct", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == new_distinct_attribute
    response = await fastapi_test_client.delete(f"/indexes/attributes/distinct/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == default_distinct_attribute


async def test_get_searchable_attributes(fastapi_test_client, async_empty_index, small_movies):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]
    data = {"uid": uid, "documents": small_movies, "primaryKey": "id"}
    response = await fastapi_test_client.put("/documents", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]


async def test_update_searchable_attributes(
    fastapi_test_client, async_empty_index, new_searchable_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "searchableAttributes": new_searchable_attributes}
    response = await fastapi_test_client.patch("/indexes/searchable-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == new_searchable_attributes


async def test_reset_searchable_attributes(
    fastapi_test_client, async_empty_index, new_searchable_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "searchableAttributes": new_searchable_attributes}
    response = await fastapi_test_client.patch("/indexes/searchable-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == new_searchable_attributes
    response = await fastapi_test_client.delete(f"/indexes/searchable-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]


async def test_get_displayed_attributes(fastapi_test_client, async_empty_index, small_movies):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]
    data = {"uid": uid, "documents": small_movies}
    update = await fastapi_test_client.put("/documents", json=data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]


async def test_update_displayed_attributes(
    fastapi_test_client, async_empty_index, displayed_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "displayedAttributes": displayed_attributes}
    response = await fastapi_test_client.patch("/indexes/displayed-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert sorted(response.json()["displayedAttributes"]) == sorted(displayed_attributes)


async def test_reset_displayed_attributes(
    fastapi_test_client, async_empty_index, displayed_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "displayedAttributes": displayed_attributes}
    response = await fastapi_test_client.patch("/indexes/displayed-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert sorted(response.json()["displayedAttributes"]) == sorted(displayed_attributes)
    response = await fastapi_test_client.delete(f"/indexes/displayed-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]


async def test_get_stop_words_default(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"indexes/stop-words/{uid}")
    assert response.json()["stopWords"] is None


async def test_update_stop_words(fastapi_test_client, async_empty_index, new_stop_words):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "stopWords": new_stop_words}
    response = await fastapi_test_client.patch("/indexes/stop-words", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"indexes/stop-words/{uid}")
    assert sorted(response.json()["stopWords"]) == sorted(new_stop_words)


async def test_reset_stop_words(fastapi_test_client, async_empty_index, new_stop_words):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "stopWords": new_stop_words}
    response = await fastapi_test_client.patch("/indexes/stop-words", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"indexes/stop-words/{uid}")
    assert sorted(response.json()["stopWords"]) == sorted(new_stop_words)
    response = await fastapi_test_client.delete(f"indexes/stop-words/{uid}")
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"indexes/stop-words/{uid}")
    assert response.json()["stopWords"] is None


async def test_get_synonyms_default(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] is None


async def test_update_synonyms(fastapi_test_client, async_empty_index, new_synonyms):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "synonyms": new_synonyms}
    response = await fastapi_test_client.patch("/indexes/synonyms", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] == new_synonyms


async def test_update_synonyms_none_provided(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    data = {"uid": uid}
    response = await fastapi_test_client.patch("/indexes/synonyms", json=data)
    assert response.status_code == 400


async def test_reset_synonyms(fastapi_test_client, async_empty_index, new_synonyms):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "synonyms": new_synonyms}
    response = await fastapi_test_client.patch("/indexes/synonyms", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] == new_synonyms
    response = await fastapi_test_client.delete(f"/indexes/synonyms/{uid}")
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] is None


async def test_get_faceting(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/faceting/{uid}")
    assert response.json()["maxValuesPerFacet"] == 100


async def test_update_faceting(fastapi_test_client, async_empty_index, faceting):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "max_values_per_facet": 90}
    response = await fastapi_test_client.patch("indexes/faceting", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/faceting/{uid}")
    assert response.json()["maxValuesPerFacet"] == faceting


async def test_reset_faceting(fastapi_test_client, async_empty_index, faceting):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "maxValuesPerFacet": faceting}
    response = await fastapi_test_client.patch("indexes/faceting", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/faceting/{uid}")
    assert response.json()["maxValuesPerFacet"] == faceting
    response = await fastapi_test_client.delete(f"/indexes/faceting/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/faceting/{uid}")
    assert response.json() == {"maxValuesPerFacet": 100}


async def test_get_filterable_attributes(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert response.json()["filterableAttributes"] is None


async def test_update_filterable_attributes(
    fastapi_test_client, async_empty_index, filterable_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "filterableAttributes": filterable_attributes}
    response = await fastapi_test_client.patch("indexes/filterable-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert sorted(response.json()["filterableAttributes"]) == filterable_attributes


async def test_reset_filterable_attributes(
    fastapi_test_client, async_empty_index, filterable_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "filterableAttributes": filterable_attributes}
    response = await fastapi_test_client.patch("indexes/filterable-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert sorted(response.json()["filterableAttributes"]) == filterable_attributes
    response = await fastapi_test_client.delete(f"/indexes/filterable-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert response.json()["filterableAttributes"] is None


async def test_get_sortable_attributes(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == []


async def test_update_sortable_attributes(
    fastapi_test_client, async_empty_index, sortable_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "sortableAttributes": sortable_attributes}
    response = await fastapi_test_client.patch("indexes/sortable-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == sortable_attributes


async def test_reset_sortable_attributes(
    fastapi_test_client, async_empty_index, sortable_attributes
):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "sortableAttributes": sortable_attributes}
    response = await fastapi_test_client.patch("indexes/sortable-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == sortable_attributes
    response = await fastapi_test_client.delete(f"/indexes/sortable-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["taskUid"])
    response = await fastapi_test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == []


async def test_typo_tolerance_default(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    response = await fastapi_test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"]["enabled"] is True


async def test_update_typo_tolerance(fastapi_test_client, async_empty_index, new_typo_tolerance):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "typo_tolerance": new_typo_tolerance}
    response = await fastapi_test_client.patch("/indexes/typo-tolerance", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"] == new_typo_tolerance


async def test_update_typo_tolerance_none_provided(fastapi_test_client, async_empty_index):
    uid = str(uuid4())
    await async_empty_index(uid)
    data = {"uid": uid}
    response = await fastapi_test_client.patch("/indexes/typo-tolerance", json=data)
    assert response.status_code == 400


async def test_reset_typo_tolerance(fastapi_test_client, async_empty_index, new_typo_tolerance):
    uid = str(uuid4())
    index = await async_empty_index(uid)
    data = {"uid": uid, "typo_tolerance": new_typo_tolerance}
    response = await fastapi_test_client.patch("/indexes/typo-tolerance", json=data)
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"] == new_typo_tolerance
    response = await fastapi_test_client.delete(f"/indexes/typo-tolerance/{uid}")
    update = await wait_for_task(index.http_client, response.json()["taskUid"])
    assert update.status == "succeeded"
    response = await fastapi_test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"]["enabled"] is True
