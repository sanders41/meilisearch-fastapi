import pytest


@pytest.fixture
def default_settings():
    return {
        "synonyms": {},
        "stopWords": [],
        "rankingRules": ["words", "typo", "proximity", "attribute", "exactness"],
        "filterableAttributes": [],
        "distinctAttribute": None,
        "searchableAttributes": ["*"],
        "displayedAttributes": ["*"],
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
    }
    response = await test_client.post("/settings", json=update_settings)

    assert response.status_code == 200

    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200

    returned_settings = response.json()

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = returned_settings["filterableAttributes"].sort()
    update_settings.pop("uid")

    assert response.json() == update_settings

    response = await test_client.delete(f"/settings/{index_uid}")

    assert response.status_code == 200

    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    returned_settings = response.json()

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = returned_settings["filterableAttributes"].sort()
    assert response.json() == default_settings
