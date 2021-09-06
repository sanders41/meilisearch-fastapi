import pytest


@pytest.fixture
def default_settings():
    return {
        "synonyms": {},
        "stopWords": [],
        "rankingRules": ["words", "typo", "sort", "proximity", "attribute", "exactness"],
        "filterableAttributes": [],
        "distinctAttribute": None,
        "searchableAttributes": ["*"],
        "displayedAttributes": ["*"],
        "sortableAttributes": [],
    }


@pytest.mark.asyncio
async def test_settings_get(default_settings, index_uid, indexes_sample, test_client):
    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    assert response.json() == default_settings


@pytest.mark.asyncio
async def test_settings_update_and_delete(default_settings, index_uid, test_client):
    update_settings = {
        "uid": index_uid,
        "synonyms": {"wolverine": ["logan", "xmen"], "logan": ["wolverine", "xmen"]},
        "stopWords": ["stop", "words"],
        "rankingRules": ["words", "typo", "proximity"],
        "filterableAttributes": ["attributes", "filterable"],
        "distinctAttribute": "movie_id",
        "searchableAttributes": ["description", "title"],
        "displayedAttributes": ["genre", "title"],
        "sortableAttributes": ["genre", "title"],
    }
    response = await test_client.post("/settings", json=update_settings)

    assert response.status_code == 200

    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200

    returned_settings = response.json()

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = sorted(returned_settings["filterableAttributes"])
    update_settings.pop("uid")

    assert returned_settings == update_settings

    response = await test_client.delete(f"/settings/{index_uid}")

    assert response.status_code == 200

    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    returned_settings = response.json()

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = sorted(returned_settings["filterableAttributes"])
    assert response.json() == default_settings
