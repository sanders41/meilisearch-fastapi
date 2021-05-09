import pytest


@pytest.mark.asyncio
async def test_get_keys(test_client, event_loop):
    response = await test_client.get("/meilisearch/keys")

    assert response.status_code == 200
    assert "public" in response.json()
    assert "private" in response.json()


@pytest.mark.asyncio
async def test_get_stats(test_client, event_loop):
    response = await test_client.get("meilisearch/stats")

    assert response.status_code == 200
    assert "databaseSize" in response.json()
    assert "lastUpdate" in response.json()
    assert "indexes" in response.json()


@pytest.mark.asyncio
async def test_get_version(test_client, event_loop):
    response = await test_client.get("meilisearch/version")

    assert response.status_code == 200
    assert "commitSha" in response.json()
    assert "buildDate" in response.json()
    assert "pkgVersion" in response.json()
