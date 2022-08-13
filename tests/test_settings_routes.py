import pytest
from meilisearch_python_async.task import wait_for_task


@pytest.fixture
def default_settings():
    return {
        "synonyms": {},
        "stopWords": [],
        "rankingRules": ["words", "typo", "proximity", "attribute", "sort", "exactness"],
        "filterableAttributes": [],
        "faceting": {"maxValuesPerFacet": 100},
        "distinctAttribute": None,
        "searchableAttributes": ["*"],
        "displayedAttributes": ["*"],
        "sortableAttributes": [],
        "typoTolerance": {
            "enabled": True,
            "disableOnAttributes": [],
            "disableOnWords": [],
            "minWordSizeForTypos": {"oneTypo": 5, "twoTypos": 9},
        },
    }


@pytest.mark.usefixtures("indexes_sample")
async def test_settings_get(default_settings, index_uid, test_client):
    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    assert response.json() == default_settings


@pytest.mark.usefixtures("indexes_sample")
async def test_settings_update_and_delete(default_settings, index_uid, test_client, raw_client):
    update_settings = {
        "uid": index_uid,
        "synonyms": {"logan": ["wolverine", "xmen"], "wolverine": ["logan", "xmen"]},
        "stopWords": ["stop", "words"],
        "rankingRules": ["words", "typo", "proximity"],
        "filterableAttributes": ["attributes", "filterable"],
        "faceting": {"maxValuesPerFacet": 90},
        "distinctAttribute": "movie_id",
        "searchableAttributes": ["description", "title"],
        "displayedAttributes": ["genre", "title"],
        "sortableAttributes": ["genre", "title"],
        "typoTolerance": {
            "enabled": False,
        },
    }
    response = await test_client.patch("/settings", json=update_settings)

    assert response.status_code == 200
    await wait_for_task(raw_client.http_client, response.json()["taskUid"])

    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200

    returned_settings = response.json()

    assert returned_settings["typoTolerance"]["enabled"] is False

    del returned_settings["typoTolerance"]

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = sorted(returned_settings["filterableAttributes"])
    update_settings.pop("uid")
    update_settings.pop("typoTolerance")

    assert returned_settings == update_settings

    response = await test_client.delete(f"/settings/{index_uid}")

    assert response.status_code == 200

    response = await test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    returned_settings = response.json()

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = sorted(returned_settings["filterableAttributes"])
    assert response.json() == default_settings
