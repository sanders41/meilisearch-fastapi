from uuid import uuid4

import pytest
from meilisearch_python_async.task import wait_for_task


async def test_basic_search(fastapi_test_client, async_index_with_documents, small_movies):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {"uid": uid, "query": "How to Train Your Dragon"}
    response = await fastapi_test_client.post("/search", json=data)
    assert response.json()["hits"][0]["id"] == "166428"
    assert "_formatted" not in response.json()["hits"][0]


async def test_search_with_empty_query(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {"uid": uid, "query": ""}
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 20
    assert response.json()["query"] == ""


async def test_custom_search(fastapi_test_client, async_index_with_documents, small_movies):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {"uid": uid, "query": "Dragon", "attributesToHighlight": ["title"]}
    response = await fastapi_test_client.post("/search", json=data)
    assert response.json()["hits"][0]["id"] == "166428"
    assert "_formatted" in response.json()["hits"][0]
    assert "dragon" in response.json()["hits"][0]["_formatted"]["title"].lower()


async def test_custom_search_with_empty_query(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {"uid": uid, "query": "", "attributesToHighlight": ["title"]}
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 20
    assert response.json()["query"] == ""


async def test_custom_search_with_no_query(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {"uid": uid, "query": "", "limit": 5}
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 5


async def test_custom_search_params_with_wildcard(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {
        "uid": uid,
        "query": "a",
        "limit": 5,
        "attributesToHightlight": ["*"],
        "attributesToRetrieve": ["*"],
        "attributesToCrop": ["*"],
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 5
    assert "_formatted" in response.json()["hits"][0]
    assert "title" in response.json()["hits"][0]["_formatted"]


async def test_custom_search_params_with_simple_string(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {
        "uid": uid,
        "query": "a",
        "limit": 5,
        "attributesToHightlight": ["title"],
        "attributesToRetrieve": ["title"],
        "attributesToCrop": ["title"],
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 5
    assert "_formatted" in response.json()["hits"][0]
    assert "title" in response.json()["hits"][0]["_formatted"]
    assert "release_date" not in response.json()["hits"][0]["_formatted"]


async def test_custom_search_params_with_string_list(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {
        "uid": uid,
        "query": "a",
        "limit": 5,
        "attributesToRetrieve": ["title", "overview"],
        "attributesToHighlight": ["title"],
    }
    response = await fastapi_test_client.post("/search", json=data)

    assert len(response.json()["hits"]) == 5
    assert "title" in response.json()["hits"][0]
    assert "overview" in response.json()["hits"][0]
    assert "release_date" not in response.json()["hits"][0]
    assert "<em>" in response.json()["hits"][0]["_formatted"]["title"]
    assert "<em>" not in response.json()["hits"][0]["_formatted"]["overview"]


async def test_custom_search_params_with_facet_distribution(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    index = await async_index_with_documents(small_movies, uid)
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await fastapi_test_client.patch("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    data = {
        "uid": uid,
        "query": "world",
        "facets": ["genre"],
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 12
    assert response.json()["facetDistribution"] is not None
    assert "genre" in response.json()["facetDistribution"]
    assert response.json()["facetDistribution"]["genre"]["cartoon"] == 1
    assert response.json()["facetDistribution"]["genre"]["action"] == 3
    assert response.json()["facetDistribution"]["genre"]["fantasy"] == 1


async def test_custom_search_params_with_facet_filters(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    index = await async_index_with_documents(small_movies, uid)
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await fastapi_test_client.patch("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    data = {
        "uid": uid,
        "query": "world",
        "filter": [["genre = action"]],
    }

    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 3
    assert response.json()["facetDistribution"] is None


async def test_custom_search_params_with_multiple_facet_filters(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    index = await async_index_with_documents(small_movies, uid)
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await fastapi_test_client.patch("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    data = {
        "uid": uid,
        "query": "world",
        "filter": ["genre = action", ["genre = action", "genre = action"]],
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 3
    assert response.json()["facetDistribution"] is None


async def test_custom_search_facet_filters_with_space(fastapi_test_client, async_empty_index):
    dataset = [
        {
            "id": 123,
            "title": "Pride and Prejudice",
            "comment": "A great book",
            "genre": "romance",
        },
        {
            "id": 456,
            "title": "Le Petit Prince",
            "comment": "A french book about a prince that walks on little cute planets",
            "genre": "adventure",
        },
        {
            "id": 2,
            "title": "Le Rouge et le Noir",
            "comment": "Another french book",
            "genre": "romance",
        },
        {
            "id": 1,
            "title": "Alice In Wonderland",
            "comment": "A weird book",
            "genre": "adventure",
        },
        {
            "id": 1344,
            "title": "The Hobbit",
            "comment": "An awesome book",
            "genre": "sci fi",
        },
        {
            "id": 4,
            "title": "Harry Potter and the Half-Blood Prince",
            "comment": "The best book",
            "genre": "fantasy",
        },
        {"id": 42, "title": "The Hitchhiker's Guide to the Galaxy", "genre": "fantasy"},
    ]

    uid = str(uuid4())
    index = await async_empty_index(uid)
    documents = {
        "uid": uid,
        "documents": dataset,
    }
    update = await fastapi_test_client.post("/documents", json=documents)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await fastapi_test_client.patch("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    data = {
        "uid": uid,
        "query": "h",
        "filter": ["genre = 'sci fi'"],
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 1
    assert response.json()["hits"][0]["title"] == "The Hobbit"


async def test_custom_search_params_with_many_params(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    index = await async_index_with_documents(small_movies, uid)
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await fastapi_test_client.patch("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["taskUid"])
    data = {
        "uid": uid,
        "query": "world",
        "filter": [["genre = action"]],
        "attributesToRetrieve": ["title", "poster"],
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 3
    assert response.json()["facetDistribution"] is None
    assert "title" in response.json()["hits"][0]
    assert "poster" in response.json()["hits"][0]
    assert "overview" not in response.json()["hits"][0]
    assert "release_date" not in response.json()["hits"][0]
    assert response.json()["hits"][0]["title"] == "Avengers: Infinity War"


@pytest.mark.parametrize(
    "sort, titles",
    [
        (
            ["title:asc"],
            ["After", "Us"],
        ),
        (
            ["title:desc"],
            ["Us", "After"],
        ),
    ],
)
async def test_search_sort(
    sort, titles, fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    index = await async_index_with_documents(small_movies, uid)
    response = await index.update_sortable_attributes(["title"])
    await wait_for_task(index.http_client, response.task_uid)
    stats = await index.get_stats()  # get this to get the total document count

    # Using a placeholder search because ranking rules affect sort otherwaise meaning the results
    # will almost never be in alphabetical order.
    data = {
        "uid": uid,
        "sort": sort,
        "limit": stats.number_of_documents,
    }
    response = await fastapi_test_client.post("/search", json=data)

    assert response.json()["hits"][0]["title"] == titles[0]
    assert response.json()["hits"][stats.number_of_documents - 1]["title"] == titles[1]


async def test_custom_search_hightlight_tags_and_crop_marker(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {
        "uid": uid,
        "query": "Dragon",
        "crop_length": 5,
        "attributes_to_highlight": ["title"],
        "highlight_pre_tag": "<strong>",
        "highlight_post_tag": "</strong>",
        "crop_marker": "***",
    }
    response = await fastapi_test_client.post("/search", json=data)
    assert response.json()["hits"][0]["id"] == "166428"
    assert "_formatted" in response.json()["hits"][0]
    assert "dragon" in response.json()["hits"][0]["_formatted"]["title"].lower()
    assert "<strong>" in response.json()["hits"][0]["_formatted"]["title"]
    assert "</strong>" in response.json()["hits"][0]["_formatted"]["title"]


async def test_custom_search_params_with_matching_strategy_all(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {
        "uid": uid,
        "query": "man loves",
        "limit": 5,
        "matchingStrategy": "all",
    }

    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 1


async def test_custom_search_params_with_matching_strategy_last(
    fastapi_test_client, async_index_with_documents, small_movies
):
    uid = str(uuid4())
    await async_index_with_documents(small_movies, uid)
    data = {
        "uid": uid,
        "query": "man loves",
        "limit": 5,
        "matchingStrategy": "last",
    }

    response = await fastapi_test_client.post("/search", json=data)
    assert len(response.json()["hits"]) > 1
