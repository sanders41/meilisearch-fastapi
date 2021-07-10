import pytest
from meilisearch_python_async.models import MeiliSearchSettings


@pytest.fixture
def new_settings():
    return MeiliSearchSettings(
        ranking_rules=["typo", "words"], searchable_attributes=["title", "overview"]
    )


@pytest.fixture
def default_ranking_rules():
    return ["words", "typo", "proximity", "attribute", "exactness"]


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
def filterable_attributes():
    return ["release_date", "title"]


@pytest.mark.asyncio
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


@pytest.mark.asyncio
@pytest.mark.usefixtures("indexes_sample")
async def test_get_index(test_client, index_uid):
    response = await test_client.get(f"/indexes/{index_uid}")
    assert response.json()["uid"] == index_uid


@pytest.mark.asyncio
async def test_get_index_none(test_client):
    response = await test_client.get("/indexes/bad")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.usefixtures("indexes_sample")
async def test_get_indexes(test_client, index_uid, index_uid2):
    response = await test_client.get("/indexes")
    response_uids = [x["uid"] for x in response.json()]

    assert index_uid in response_uids
    assert index_uid2 in response_uids
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_indexes_none(test_client):
    response = await test_client.get("/indexes")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.usefixtures("indexes_sample")
async def test_get_primary_key(test_client, index_uid2):
    response = await test_client.get(f"/indexes/primary-key/{index_uid2}")
    assert response.json()["primaryKey"] == "book_id"


@pytest.mark.asyncio
@pytest.mark.usefixtures("indexes_sample")
async def test_delete_index(test_client, index_uid, index_uid2):
    response = await test_client.delete(f"indexes/{index_uid}")
    assert response.status_code == 204

    response = await test_client.get(f"/indexes/{index_uid}")
    assert response.status_code == 404

    response = await test_client.delete(f"indexes/{index_uid2}")
    assert response.status_code == 204

    response = await test_client.get(f"/indexes/{index_uid2}")
    assert response.status_code == 404

    response = await test_client.get("/indexes")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.usefixtures("indexes_sample")
@pytest.mark.parametrize("test_uid", ["indexUID", "none"])
async def test_delete_if_exists(test_client, test_uid):
    response = await test_client.delete(f"/indexes/delete-if-exists/{test_uid}")
    assert response.status_code == 204

    response = await test_client.get(f"/indexes/{test_uid}")
    assert response.status_code == 404


@pytest.mark.asyncio
@pytest.mark.usefixtures("indexes_sample")
async def test_update_index(test_client, index_uid):
    primay_key = "objectID"
    update_data = {"uid": index_uid, "primaryKey": primay_key}
    response = await test_client.put("/indexes", json=update_data)
    response_primary_key = response.json()["primaryKey"]

    assert response_primary_key == primay_key


@pytest.mark.asyncio
async def test_get_stats(test_client, empty_index, small_movies):
    uid, index = empty_index
    data = {"uid": uid, "documents": small_movies}
    update = await test_client.put("/documents", json=data)
    await index.wait_for_pending_update(update.json()["updateId"])
    response = await test_client.get(f"/indexes/stats/{uid}")

    assert response.json()["numberOfDocuments"] == 30


@pytest.mark.asyncio
async def test_get_ranking_rules_default(test_client, empty_index, default_ranking_rules):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == default_ranking_rules


@pytest.mark.asyncio
async def test_update_ranking_rules(test_client, empty_index, new_ranking_rules):
    uid, index = empty_index
    data = {"uid": uid, "rankingRules": new_ranking_rules}
    response = await test_client.put("/indexes/ranking-rules", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == new_ranking_rules


@pytest.mark.asyncio
async def test_reset_ranking_rules(
    test_client, empty_index, new_ranking_rules, default_ranking_rules
):
    uid, index = empty_index
    data = {"uid": uid, "rankingRules": new_ranking_rules}
    response = await test_client.put("/indexes/ranking-rules", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == new_ranking_rules
    response = await test_client.delete(f"/indexes/ranking-rules/{uid}")
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/ranking-rules/{uid}")
    ranking_rules = response.json()["rankingRules"]
    assert ranking_rules == default_ranking_rules


@pytest.mark.asyncio
async def test_get_distinct_attribute(test_client, empty_index, default_distinct_attribute):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == default_distinct_attribute


@pytest.mark.asyncio
async def test_update_distinct_attribute(test_client, empty_index, new_distinct_attribute):
    uid, index = empty_index
    data = {"uid": uid, "attribute": new_distinct_attribute}
    response = await test_client.put("/indexes/attributes/distinct", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == new_distinct_attribute


@pytest.mark.asyncio
async def test_reset_distinct_attribute(
    test_client, empty_index, new_distinct_attribute, default_distinct_attribute
):
    uid, index = empty_index
    data = {"uid": uid, "attribute": new_distinct_attribute}
    response = await test_client.put("/indexes/attributes/distinct", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == new_distinct_attribute
    response = await test_client.delete(f"/indexes/attributes/distinct/{uid}")
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/attributes/distinct/{uid}")
    assert response.json()["attribute"] == default_distinct_attribute


@pytest.mark.asyncio
async def test_get_searchable_attributes(test_client, empty_index, small_movies):
    uid, index = empty_index
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]
    data = {"uid": uid, "documents": small_movies, "primaryKey": "id"}
    response = await test_client.put("/documents", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]


@pytest.mark.asyncio
async def test_update_searchable_attributes(test_client, empty_index, new_searchable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "searchableAttributes": new_searchable_attributes}
    response = await test_client.put("/indexes/searchable-attributes", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == new_searchable_attributes


@pytest.mark.asyncio
async def test_reset_searchable_attributes(test_client, empty_index, new_searchable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "searchableAttributes": new_searchable_attributes}
    response = await test_client.put("/indexes/searchable-attributes", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == new_searchable_attributes
    response = await test_client.delete(f"/indexes/searchable-attributes/{uid}")
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/searchable-attributes/{uid}")
    assert response.json()["searchableAttributes"] == ["*"]


@pytest.mark.asyncio
async def test_get_displayed_attributes(test_client, empty_index, small_movies):
    uid, index = empty_index
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]
    data = {"uid": uid, "documents": small_movies}
    update = await test_client.put("/documents", json=data)
    await index.wait_for_pending_update(update.json()["updateId"])
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]


@pytest.mark.asyncio
async def test_update_displayed_attributes(test_client, empty_index, displayed_attributes):
    uid, index = empty_index
    data = {"uid": uid, "displayedAttributes": displayed_attributes}
    response = await test_client.put("/indexes/displayed-attributes", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert sorted(response.json()["displayedAttributes"]) == sorted(displayed_attributes)


@pytest.mark.asyncio
async def test_reset_displayed_attributes(test_client, empty_index, displayed_attributes):
    uid, index = empty_index
    data = {"uid": uid, "displayedAttributes": displayed_attributes}
    response = await test_client.put("/indexes/displayed-attributes", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert sorted(response.json()["displayedAttributes"]) == sorted(displayed_attributes)
    response = await test_client.delete(f"/indexes/displayed-attributes/{uid}")
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/displayed-attributes/{uid}")
    assert response.json()["displayedAttributes"] == ["*"]


@pytest.mark.asyncio
async def test_get_stop_words_default(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert response.json()["stopWords"] is None


@pytest.mark.asyncio
async def test_update_stop_words(test_client, empty_index, new_stop_words):
    uid, index = empty_index
    data = {"uid": uid, "stopWords": new_stop_words}
    response = await test_client.put("/indexes/stop-words", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert sorted(response.json()["stopWords"]) == sorted(new_stop_words)


@pytest.mark.asyncio
async def test_reset_stop_words(test_client, empty_index, new_stop_words):
    uid, index = empty_index
    data = {"uid": uid, "stopWords": new_stop_words}
    response = await test_client.put("/indexes/stop-words", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert sorted(response.json()["stopWords"]) == sorted(new_stop_words)
    response = await test_client.delete(f"indexes/stop-words/{uid}")
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"indexes/stop-words/{uid}")
    assert response.json()["stopWords"] is None


@pytest.mark.asyncio
async def test_get_synonyms_default(test_client, empty_index):
    uid, index = empty_index
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] is None


@pytest.mark.asyncio
async def test_update_synonyms(test_client, empty_index, new_synonyms):
    uid, index = empty_index
    data = {"uid": uid, "synonyms": new_synonyms}
    response = await test_client.put("/indexes/synonyms", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] == new_synonyms


@pytest.mark.asyncio
async def test_update_synonyms_none_provided(test_client, empty_index, new_synonyms):
    uid, _ = empty_index
    data = {"uid": uid}
    response = await test_client.put("/indexes/synonyms", json=data)
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_reset_synonyms(test_client, empty_index, new_synonyms):
    uid, index = empty_index
    data = {"uid": uid, "synonyms": new_synonyms}
    response = await test_client.put("/indexes/synonyms", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] == new_synonyms
    response = await test_client.delete(f"/indexes/synonyms/{uid}")
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/synonyms/{uid}")
    assert response.json()["synonyms"] is None


@pytest.mark.asyncio
async def test_get_filterable_attributes(test_client, empty_index):
    uid, _ = empty_index
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert response.json()["filterableAttributes"] is None


@pytest.mark.asyncio
async def test_update_filterable_attributes(test_client, empty_index, filterable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "filterableAttributes": filterable_attributes}
    response = await test_client.put("indexes/filterable-attributes", json=data)
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert sorted(response.json()["filterableAttributes"]) == filterable_attributes


@pytest.mark.asyncio
async def test_reset_filterable_attributes(test_client, empty_index, filterable_attributes):
    uid, index = empty_index
    data = {"uid": uid, "filterableAttributes": filterable_attributes}
    response = await test_client.put("indexes/filterable-attributes", json=data)
    update = await index.wait_for_pending_update(response.json()["updateId"])
    assert update.status == "processed"
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert sorted(response.json()["filterableAttributes"]) == filterable_attributes
    response = await test_client.delete(f"/indexes/filterable-attributes/{uid}")
    await index.wait_for_pending_update(response.json()["updateId"])
    response = await test_client.get(f"/indexes/filterable-attributes/{uid}")
    assert response.json()["filterableAttributes"] is None
