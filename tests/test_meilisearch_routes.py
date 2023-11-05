from datetime import datetime, timedelta, timezone

import jwt
import pytest
from meilisearch_python_sdk.errors import MeilisearchApiError
from meilisearch_python_sdk.models.client import KeyCreate


@pytest.fixture
async def test_key(async_client):
    key_info = KeyCreate(description="test", actions=["search"], indexes=["movies"])
    key = await async_client.create_key(key_info)

    yield key

    try:
        await async_client.delete_key(key.key)
    except MeilisearchApiError:
        pass


@pytest.fixture
async def test_key_info(async_client):
    key_info = KeyCreate(description="test", actions=["search"], indexes=["movies"])

    yield key_info

    try:
        keys = await async_client.get_keys()
        key = next(x for x in keys.results if x.description == key_info.description)
        await async_client.delete_key(key.key)
    except MeilisearchApiError:
        pass


async def test_generate_tenant_token(fastapi_test_client, default_search_key):
    search_rules = {"test": "value"}
    expected = {"searchRules": search_rules, "apiKeyUid": default_search_key.uid}
    api_key = default_search_key.model_dump()
    api_key["created_at"] = f"{api_key['created_at'].isoformat()}Z"
    api_key["updated_at"] = f"{api_key['updated_at'].isoformat()}Z"
    payload = {
        "search_rules": search_rules,
        "api_key": api_key,
    }
    response = await fastapi_test_client.post("/meilisearch/generate-tenant-token", json=payload)
    token = response.json()["tenantToken"]

    assert expected == jwt.decode(jwt=token, key=default_search_key.key, algorithms=["HS256"])


async def test_generate_tenant_token_expires(fastapi_test_client, default_search_key):
    search_rules = {"test": "value"}
    expires_at = datetime.now(tz=timezone.utc) + timedelta(days=1)
    expected = {"searchRules": search_rules, "apiKeyUid": default_search_key.uid}
    expected["exp"] = int(datetime.timestamp(expires_at))  # type: ignore
    api_key = default_search_key.model_dump()
    api_key["created_at"] = f"{api_key['created_at'].isoformat()}Z"
    api_key["updated_at"] = f"{api_key['updated_at'].isoformat()}Z"
    payload = {
        "search_rules": search_rules,
        "api_key": api_key,
        "expires_at": expires_at.isoformat(),
    }
    response = await fastapi_test_client.post("/meilisearch/generate-tenant-token", json=payload)
    token = response.json()["tenantToken"]

    assert expected == jwt.decode(jwt=token, key=default_search_key.key, algorithms=["HS256"])


async def test_generate_tenant_token_default_key_expires_past(
    fastapi_test_client, default_search_key
):
    search_rules = {"test": "value"}
    expires_at = datetime.now(tz=timezone.utc) + timedelta(days=-1)
    api_key = default_search_key.model_dump()
    api_key["created_at"] = f"{api_key['created_at'].isoformat()}Z"
    api_key["updated_at"] = f"{api_key['updated_at'].isoformat()}Z"
    payload = {
        "search_rules": search_rules,
        "api_key": api_key,
        "expires_at": expires_at.isoformat(),
    }
    response = await fastapi_test_client.post("/meilisearch/generate-tenant-token", json=payload)

    assert response.status_code == 400


async def test_generate_tenant_token_invalid_restriction(
    test_key_info, fastapi_test_client, async_client
):
    test_key_info.indexes = ["good"]
    key = await async_client.create_key(test_key_info)
    api_key = key.model_dump()
    api_key["created_at"] = f"{api_key['created_at'].isoformat()}Z"
    api_key["updated_at"] = f"{api_key['updated_at'].isoformat()}Z"
    payload = {"search_rules": {"indexes": ["bad"]}, "api_key": api_key}

    response = await fastapi_test_client.post("/meilisearch/generate-tenant-token", json=payload)

    assert response.status_code == 400


async def test_get_health(fastapi_test_client):
    response = await fastapi_test_client.get("/meilisearch/health")
    assert response.json() == {"status": "available"}


@pytest.mark.parametrize(
    "expires_at",
    (
        None,
        f"{(datetime.now(tz=timezone.utc) + timedelta(days=2)).isoformat()}",
    ),
)
async def test_create_key(expires_at, fastapi_test_client, test_key_info):
    info = test_key_info.model_dump()
    if expires_at:
        info["expires_at"] = expires_at

    key = await fastapi_test_client.post("/meilisearch/keys", json=info)
    key_info = key.json()

    assert key_info["description"] == test_key_info.description
    assert key_info["actions"] == test_key_info.actions
    assert key_info["indexes"] == test_key_info.indexes

    if expires_at:
        assert key_info["expiresAt"] is not None
    else:
        assert key_info["expiresAt"] is None


async def test_delete_key(test_key, fastapi_test_client, async_client):
    result = await fastapi_test_client.delete(f"/meilisearch/keys/{test_key.key}")
    assert result.status_code == 204

    with pytest.raises(MeilisearchApiError):
        await async_client.get_key(test_key.key)


async def test_get_keys(fastapi_test_client):
    response = await fastapi_test_client.get("/meilisearch/keys")

    assert response.status_code == 200
    assert len(response.json()["results"]) == 2


async def test_get_key(test_key, fastapi_test_client):
    response = await fastapi_test_client.get(f"/meilisearch/keys/{test_key.key}")
    assert response.json()["description"] == test_key.description


async def test_update_key(test_key, fastapi_test_client):
    update_key_info = {
        "key": test_key.key,
        "name": "Updated Name",
        "description": "updated",
    }

    key = await fastapi_test_client.patch(f"meilisearch/keys/{test_key.key}", json=update_key_info)
    key_info = key.json()

    assert key_info["name"] == update_key_info["name"]
    assert key_info["description"] == update_key_info["description"]


async def test_get_stats(fastapi_test_client):
    response = await fastapi_test_client.get("meilisearch/stats")

    assert response.status_code == 200
    assert "databaseSize" in response.json()
    assert "lastUpdate" in response.json()
    assert "indexes" in response.json()


async def test_get_version(fastapi_test_client):
    response = await fastapi_test_client.get("meilisearch/version")

    assert response.status_code == 200
    assert "commitSha" in response.json()
    assert "commitDate" in response.json()
    assert "pkgVersion" in response.json()
