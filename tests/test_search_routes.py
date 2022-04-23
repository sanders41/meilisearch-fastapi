import pytest
from meilisearch_python_async.task import wait_for_task


async def test_basic_search(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {"uid": uid, "query": "How to Train Your Dragon"}
    response = await test_client.post("/search", json=data)
    assert response.json()["hits"][0]["id"] == "166428"
    assert "_formatted" not in response.json()["hits"][0]


async def test_search_with_empty_query(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {"uid": uid, "query": ""}
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 20
    assert response.json()["query"] == ""


async def test_custom_search(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {"uid": uid, "query": "Dragon", "attributesToHighlight": ["title"]}
    response = await test_client.post("/search", json=data)
    assert response.json()["hits"][0]["id"] == "166428"
    assert "_formatted" in response.json()["hits"][0]
    assert "dragon" in response.json()["hits"][0]["_formatted"]["title"].lower()


async def test_custom_search_with_empty_query(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {"uid": uid, "query": "", "attributesToHighlight": ["title"]}
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 20
    assert response.json()["query"] == ""


async def test_custom_search_with_no_query(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {"uid": uid, "query": "", "limit": 5}
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 5


async def test_custom_search_params_with_wildcard(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {
        "uid": uid,
        "query": "a",
        "limit": 5,
        "attributesToHightlight": ["*"],
        "attributesToRetrieve": ["*"],
        "attributesToCrop": ["*"],
    }
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 5
    assert "_formatted" in response.json()["hits"][0]
    assert "title" in response.json()["hits"][0]["_formatted"]


async def test_custom_search_params_with_simple_string(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {
        "uid": uid,
        "query": "a",
        "limit": 5,
        "attributesToHightlight": ["title"],
        "attributesToRetrieve": ["title"],
        "attributesToCrop": ["title"],
    }
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 5
    assert "_formatted" in response.json()["hits"][0]
    assert "title" in response.json()["hits"][0]["_formatted"]
    assert "release_date" not in response.json()["hits"][0]["_formatted"]


async def test_custom_search_params_with_string_list(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {
        "uid": uid,
        "query": "a",
        "limit": 5,
        "attributesToRetrieve": ["title", "overview"],
        "attributesToHighlight": ["title"],
    }
    response = await test_client.post("/search", json=data)

    assert len(response.json()["hits"]) == 5
    assert "title" in response.json()["hits"][0]
    assert "overview" in response.json()["hits"][0]
    assert "release_date" not in response.json()["hits"][0]
    assert "<em>" in response.json()["hits"][0]["_formatted"]["title"]
    assert "<em>" not in response.json()["hits"][0]["_formatted"]["overview"]


async def test_custom_search_params_with_facets_distribution(test_client, index_with_documents):
    uid, index = index_with_documents
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await test_client.put("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["uid"])
    data = {
        "uid": uid,
        "query": "world",
        "facetsDistribution": ["genre"],
    }
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 12
    assert response.json()["facetsDistribution"] is not None
    assert response.json()["exhaustiveFacetsCount"] is not None
    assert "genre" in response.json()["facetsDistribution"]
    assert response.json()["facetsDistribution"]["genre"]["cartoon"] == 1
    assert response.json()["facetsDistribution"]["genre"]["action"] == 3
    assert response.json()["facetsDistribution"]["genre"]["fantasy"] == 1


async def test_custom_search_params_with_facet_filters(test_client, index_with_documents):
    uid, index = index_with_documents
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await test_client.put("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["uid"])
    data = {
        "uid": uid,
        "query": "world",
        "filter": [["genre = action"]],
    }

    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 3
    assert response.json()["facetsDistribution"] is None
    assert response.json()["exhaustiveFacetsCount"] is None


async def test_custom_search_params_with_multiple_facet_filters(test_client, index_with_documents):
    uid, index = index_with_documents
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await test_client.put("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["uid"])
    data = {
        "uid": uid,
        "query": "world",
        "filter": ["genre = action", ["genre = action", "genre = action"]],
    }
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 3
    assert response.json()["facetsDistribution"] is None
    assert response.json()["exhaustiveFacetsCount"] is None


async def test_custom_search_facet_filters_with_space(test_client, empty_index):
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

    uid, index = empty_index
    documents = {
        "uid": uid,
        "documents": dataset,
    }
    update = await test_client.post("/documents", json=documents)
    await wait_for_task(index.http_client, update.json()["uid"])
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await test_client.put("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["uid"])
    data = {
        "uid": uid,
        "query": "h",
        "filter": ["genre = 'sci fi'"],
    }
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 1
    assert response.json()["hits"][0]["title"] == "The Hobbit"


async def test_custom_search_params_with_many_params(test_client, index_with_documents):
    uid, index = index_with_documents
    facet_data = {"uid": uid, "filterableAttributes": ["genre"]}
    update = await test_client.put("/indexes/filterable-attributes", json=facet_data)
    await wait_for_task(index.http_client, update.json()["uid"])
    data = {
        "uid": uid,
        "query": "world",
        "filter": [["genre = action"]],
        "attributesToRetrieve": ["title", "poster"],
    }
    response = await test_client.post("/search", json=data)
    assert len(response.json()["hits"]) == 3
    assert response.json()["facetsDistribution"] is None
    assert response.json()["exhaustiveFacetsCount"] is None
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
async def test_search_sort(sort, titles, test_client, index_with_documents):
    uid, index = index_with_documents
    response = await index.update_sortable_attributes(["title"])
    await wait_for_task(index.http_client, response.uid)
    stats = await index.get_stats()  # get this to get the total document count

    # Using a placeholder search because ranking rules affect sort otherwaise meaning the results
    # will almost never be in alphabetical order.
    data = {
        "uid": uid,
        "sort": sort,
        "limit": stats.number_of_documents,
    }
    response = await test_client.post("/search", json=data)

    assert response.json()["hits"][0]["title"] == titles[0]
    assert response.json()["hits"][stats.number_of_documents - 1]["title"] == titles[1]


async def test_custom_search_hightlight_tags_and_crop_marker(test_client, index_with_documents):
    uid, _ = index_with_documents
    data = {
        "uid": uid,
        "query": "Dragon",
        "crop_length": 5,
        "attributes_to_highlight": ["title"],
        "highlight_pre_tag": "<strong>",
        "highlight_post_tag": "</strong>",
        "crop_marker": "***",
    }
    response = await test_client.post("/search", json=data)
    assert response.json()["hits"][0]["id"] == "166428"
    assert "_formatted" in response.json()["hits"][0]
    assert "dragon" in response.json()["hits"][0]["_formatted"]["title"].lower()
    assert "<strong>" in response.json()["hits"][0]["_formatted"]["title"]
    assert "</strong>" in response.json()["hits"][0]["_formatted"]["title"]
