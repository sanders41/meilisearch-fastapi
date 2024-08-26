import pytest


@pytest.fixture
def default_settings():
    return {
        "synonyms": {},
        "stopWords": [],
        "rankingRules": ["words", "typo", "proximity", "attribute", "sort", "exactness"],
        "searchCutoffMs": None,
        "filterableAttributes": [],
        "localizedAttributes": None,
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
        "faceting": {"maxValuesPerFacet": 100, "sortFacetValuesBy": {"*": "alpha"}},
        "pagination": {"maxTotalHits": 1000},
        "dictionary": [],
        "nonSeparatorTokens": [],
        "separatorTokens": [],
        "proximityPrecision": "byWord",
        "embedders": None,
    }


@pytest.mark.usefixtures("indexes_sample")
async def test_settings_get(default_settings, index_uid, fastapi_test_client):
    response = await fastapi_test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    assert response.json() == default_settings


@pytest.mark.usefixtures("indexes_sample")
async def test_settings_update_and_delete(
    default_settings, index_uid, fastapi_test_client, async_meilisearch_client
):
    update_settings = {
        "uid": index_uid,
        "synonyms": {"logan": ["wolverine", "xmen"], "wolverine": ["logan", "xmen"]},
        "stopWords": ["stop", "words"],
        "rankingRules": ["words", "typo", "proximity"],
        "filterableAttributes": ["attributes", "filterable"],
        "localizedAttributes": None,
        "faceting": {"maxValuesPerFacet": 90, "sortFacetValuesBy": {"*": "alpha"}},
        "distinctAttribute": "movie_id",
        "searchCutoffMs": None,
        "searchableAttributes": ["description", "title"],
        "separatorTokens": ["-"],
        "nonSeparatorTokens": ["&"],
        "displayedAttributes": ["genre", "title"],
        "sortableAttributes": ["genre", "title"],
        "typoTolerance": {
            "enabled": False,
        },
        "pagination": {"maxTotalHits": 1000},
        "dictionary": ["a"],
        "proximityPrecision": "byWord",
        "embedders": None,
    }
    response = await fastapi_test_client.patch("/settings", json=update_settings)

    assert response.status_code == 200
    await async_meilisearch_client.wait_for_task(response.json()["taskUid"])

    response = await fastapi_test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200

    returned_settings = response.json()

    assert returned_settings["typoTolerance"]["enabled"] is False

    del returned_settings["typoTolerance"]

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = sorted(returned_settings["filterableAttributes"])
    update_settings.pop("uid")
    update_settings.pop("typoTolerance")

    assert returned_settings == update_settings

    response = await fastapi_test_client.delete(f"/settings/{index_uid}")

    assert response.status_code == 200

    response = await fastapi_test_client.get(f"/settings/{index_uid}")

    assert response.status_code == 200
    returned_settings = response.json()

    # Filterable attributes come back in random order so sort them to be able to compare
    returned_settings["filterableAttributes"] = sorted(returned_settings["filterableAttributes"])
    assert response.json() == default_settings
