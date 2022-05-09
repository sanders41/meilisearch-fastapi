import pytest
from meilisearch_python_async.models.settings import MeiliSearchSettings
from meilisearch_python_async.task import wait_for_task


@pytest.fixture
def new_settings():
    return MeiliSearchSettings(
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
async def test_create_index(test_client, data, expected):
    index = await test_client.post("/indexes", json=data)

    assert index.json()["uid"] == expected["uid"]
    assert index.json()["primaryKey"] == expected["primary_key"]
    assert "createdAt" in index.json()
    assert "updatedAt" in index.json()


@pytest.mark.usefixtures("indexes_sample")
async def test_get_index(test_client, index_uid):
    response = await test_client.get(f"/indexes/{index_uid}")
    assert response.json()["uid"] == index_uid


async def test_get_index_none(test_client):
    response = await test_client.get("/indexes/bad")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
async def test_get_indexes(test_client, index_uid, index_uid2):
    response = await test_client.get("/indexes")
    response_uids = [x["uid"] for x in response.json()]

    assert index_uid in response_uids
    assert index_uid2 in response_uids
    assert len(response.json()) == 2


async def test_get_indexes_none(test_client):
    response = await test_client.get("/indexes")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
async def test_get_primary_key(test_client, index_uid2):
    response = await test_client.get(f"/indexes/primary-key/{index_uid2}")
    assert response.json()["primaryKey"] == "book_id"


@pytest.mark.usefixtures("indexes_sample")
async def test_delete_index(test_client, index_uid, index_uid2, raw_client):
    response = await test_client.delete(f"indexes/{index_uid}")
    await wait_for_task(raw_client.http_client, response.json()["uid"])

    response = await test_client.get(f"/indexes/{index_uid}")
    assert response.status_code == 404

    response = await test_client.delete(f"indexes/{index_uid2}")
    await wait_for_task(raw_client.http_client, response.json()["uid"])

    response = await test_client.get(f"/indexes/{index_uid2}")
    assert response.status_code == 404

    response = await test_client.get("/indexes")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
@pytest.mark.parametrize("test_uid", ["indexUID", "none"])
async def test_delete_if_exists(test_client, test_uid):
    response = await test_client.delete(f"/indexes/delete-if-exists/{test_uid}")
    assert response.status_code == 204

    response = await test_client.get(f"/indexes/{test_uid}")
    assert response.status_code == 404


@pytest.mark.usefixtures("indexes_sample")
async def test_update_index(test_client, index_uid, raw_client):
    primay_key = "objectID"
    update_data = {"uid": index_uid, "primaryKey": primay_key}
    update = await test_client.put("/indexes", json=update_data)
    await wait_for_task(raw_client.http_client, update.json()["uid"])
    response = await test_client.get(f"/indexes/{index_uid}")
    response_primary_key = response.json()["primaryKey"]

    assert response_primary_key == primay_key


async def test_get_stats(test_client, empty_index, small_movies):
    uid, index = empty_index
    data = {"uid": uid, "documents": small_movies}
    update = await test_client.put("/documents", json=data)
    await wait_for_task(index.http_client, update.json()["uid"])
    response = await test_client.get(f"/indexes/stats/{uid}")

    assert response.json()["numberOfDocuments"] == 30


async def test_get_ranking_rules_default(test_client, empty_index, default_ranking_rules):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == default_ranking_rules


async def test_update_ranking_rules(test_client, empty_index, new_ranking_rules):
    uid, index = empty_index
    data = {"uid": uid, "rankingRules": new_ranking_rules}
    response = await test_client.put("/indexes/ranking-rules", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == new_ranking_rules


async def test_reset_ranking_rules(
    test_client, empty_index, new_ranking_rules, default_ranking_rules
):
    uid, index = empty_index
    data = {"uid": uid, "rankingRules": new_ranking_rules}
    response = await test_client.put("/indexes/ranking-rules", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == new_ranking_rules
    response = await test_client.delete(f"/indexes/ranking-rules/{uid}")
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == default_ranking_rules


async def test_get_distinct_attribute(test_client, empty_index, default_distinct_attribute):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == default_distinct_attribute


async def test_update_distinct_attribute(test_client, empty_index, new_distinct_attribute):
    uid, index = empty_index
    data = {"uid": uid, "attribute": new_distinct_attribute}
    response = await test_client.put("/indexes/attributes/distinct", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == new_distinct_attribute


async def test_reset_distinct_attribute(
    test_client, empty_index, new_distinct_attribute, default_distinct_attribute
):
    uid, index = empty_index
    data = {"uid": uid, "attribute": new_distinct_attribute}
    response = await test_client.put("/indexes/attributes/distinct", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == new_distinct_attribute
    response = await test_client.delete(f"/indexes/attributes/distinct/{uid}")
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == default_distinct_attribute


async def test_get_searchable_attributes(test_client, empty_index, small_movies):
    uid, index = empty_index
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]
    data = {"uid": uid, "documents": small_movies, "primaryKey": "id"}
    response = await test_client.put("/documents", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]


async def test_update_searchable_attributes(test_client, empty_index, new_searchable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "searchableAttributes": new_searchable_attributes}
    response = await test_client.put("/indexes/searchable-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == new_searchable_attributes


async def test_reset_searchable_attributes(test_client, empty_index, new_searchable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "searchableAttributes": new_searchable_attributes}
    response = await test_client.put("/indexes/searchable-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == new_searchable_attributes
    response = await test_client.delete(f"/indexes/searchable-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]


async def test_get_displayed_attributes(test_client, empty_index, small_movies):
    uid, index = empty_index
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]
    data = {"uid": uid, "documents": small_movies}
    update = await test_client.put("/documents", json=data)
    await wait_for_task(index.http_client, update.json()["uid"])
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]


async def test_update_displayed_attributes(test_client, empty_index, displayed_attributes):
    uid, index = empty_index
    data = {"uid": uid, "displayedAttributes": displayed_attributes}
    response = await test_client.put("/indexes/displayed-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert sorted(response.json()["displayedAttributes"]) == sorted(displayed_attributes)


async def test_reset_displayed_attributes(test_client, empty_index, displayed_attributes):
    uid, index = empty_index
    data = {"uid": uid, "displayedAttributes": displayed_attributes}
    response = await test_client.put("/indexes/displayed-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert sorted(response.json()["displayedAttributes"]) == sorted(displayed_attributes)
    response = await test_client.delete(f"/indexes/displayed-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]


async def test_get_stop_words_default(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert response.json()["stopWords"] is None


async def test_update_stop_words(test_client, empty_index, new_stop_words):
    uid, index = empty_index
    data = {"uid": uid, "stopWords": new_stop_words}
    response = await test_client.put("/indexes/stop-words", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert sorted(response.json()["stopWords"]) == sorted(new_stop_words)


async def test_reset_stop_words(test_client, empty_index, new_stop_words):
    uid, index = empty_index
    data = {"uid": uid, "stopWords": new_stop_words}
    response = await test_client.put("/indexes/stop-words", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert sorted(response.json()["stopWords"]) == sorted(new_stop_words)
    response = await test_client.delete(f"indexes/stop-words/{uid}")
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert response.json()["stopWords"] is None


async def test_get_synonyms_default(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] is None


async def test_update_synonyms(test_client, empty_index, new_synonyms):
    uid, index = empty_index
    data = {"uid": uid, "synonyms": new_synonyms}
    response = await test_client.put("/indexes/synonyms", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] == new_synonyms


async def test_update_synonyms_none_provided(test_client, empty_index):
    uid, _ = empty_index
    data = {"uid": uid}
    response = await test_client.put("/indexes/synonyms", json=data)
    assert response.status_code == 400


async def test_reset_synonyms(test_client, empty_index, new_synonyms):
    uid, index = empty_index
    data = {"uid": uid, "synonyms": new_synonyms}
    response = await test_client.put("/indexes/synonyms", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] == new_synonyms
    response = await test_client.delete(f"/indexes/synonyms/{uid}")
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] is None


async def test_get_filterable_attributes(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert response.json()["filterableAttributes"] is None


async def test_update_filterable_attributes(test_client, empty_index, filterable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "filterableAttributes": filterable_attributes}
    response = await test_client.put("indexes/filterable-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert sorted(response.json()["filterableAttributes"]) == filterable_attributes


async def test_reset_filterable_attributes(test_client, empty_index, filterable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "filterableAttributes": filterable_attributes}
    response = await test_client.put("indexes/filterable-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert sorted(response.json()["filterableAttributes"]) == filterable_attributes
    response = await test_client.delete(f"/indexes/filterable-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert response.json()["filterableAttributes"] is None


async def test_get_sortable_attributes(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == []


async def test_update_sortable_attributes(test_client, empty_index, sortable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "sortableAttributes": sortable_attributes}
    response = await test_client.put("indexes/sortable-attributes", json=data)
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == sortable_attributes


async def test_reset_sortable_attributes(test_client, empty_index, sortable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "sortableAttributes": sortable_attributes}
    response = await test_client.put("indexes/sortable-attributes", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == sortable_attributes
    response = await test_client.delete(f"/indexes/sortable-attributes/{uid}")
    await wait_for_task(index.http_client, response.json()["uid"])
    response = await test_client.get(f"/indexes/sortable-attributes/{uid}")
    assert response.json()["sortableAttributes"] == []


async def test_typo_tolerance_default(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"]["enabled"] is True


async def test_update_typo_tolerance(test_client, empty_index, new_typo_tolerance):
    uid, index = empty_index
    data = {"uid": uid, "typo_tolerance": new_typo_tolerance}
    response = await test_client.put("/indexes/typo-tolerance", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"] == new_typo_tolerance


async def test_update_typo_tolerance_none_provided(test_client, empty_index):
    uid, _ = empty_index
    data = {"uid": uid}
    response = await test_client.put("/indexes/typo-tolerance", json=data)
    assert response.status_code == 400


async def test_reset_typo_tolerance(test_client, empty_index, new_typo_tolerance):
    uid, index = empty_index
    data = {"uid": uid, "typo_tolerance": new_typo_tolerance}
    response = await test_client.put("/indexes/typo-tolerance", json=data)
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"] == new_typo_tolerance
    response = await test_client.delete(f"/indexes/typo-tolerance/{uid}")
    update = await wait_for_task(index.http_client, response.json()["uid"])
    assert update.status == "succeeded"
    response = await test_client.get(f"/indexes/typo-tolerance/{uid}")
    assert response.json()["typoTolerance"]["enabled"] is True
