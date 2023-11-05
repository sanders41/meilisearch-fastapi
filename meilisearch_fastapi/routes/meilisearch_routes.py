from fastapi import APIRouter, Depends, HTTPException
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.errors import InvalidRestriction
from meilisearch_python_sdk.models.client import (
    ClientStats,
    Key,
    KeyCreate,
    KeySearch,
    KeyUpdate,
)
from meilisearch_python_sdk.models.health import Health
from meilisearch_python_sdk.models.version import Version
from starlette.status import HTTP_204_NO_CONTENT

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi.models.tenant_token import TenantToken, TenantTokenSettings

router = APIRouter()


@router.post("/generate-tenant-token", response_model=TenantToken, tags=["Meilisearch"])
async def generate_tenant_token(
    tenant_token_settings: TenantTokenSettings, client: AsyncClient = Depends(meilisearch_client)
) -> TenantToken:
    try:
        token = client.generate_tenant_token(
            tenant_token_settings.search_rules,
            api_key=tenant_token_settings.api_key,
            expires_at=tenant_token_settings.expires_at,
        )
    except InvalidRestriction as e:
        raise HTTPException(400, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))

    return TenantToken(tenant_token=token)


@router.get("/health", response_model=Health, tags=["Meilisearch"])
async def get_health(client: AsyncClient = Depends(meilisearch_client)) -> Health:
    return await client.health()


@router.post("/keys", response_model=Key, tags=["Meilisearch"])
async def create_key(key: KeyCreate, client: AsyncClient = Depends(meilisearch_client)) -> Key:
    return await client.create_key(key)


@router.delete("/keys/{key}", status_code=HTTP_204_NO_CONTENT, tags=["Meilisearch"])
async def delete_key(key: str, client: AsyncClient = Depends(meilisearch_client)) -> None:
    await client.delete_key(key)


@router.get("/keys", response_model=KeySearch, tags=["Meilisearch"])
async def get_keys(client: AsyncClient = Depends(meilisearch_client)) -> KeySearch:
    return await client.get_keys()


@router.get("/keys/{key}", response_model=Key, tags=["Meilisearch"])
async def get_key(key: str, client: AsyncClient = Depends(meilisearch_client)) -> Key:
    return await client.get_key(key)


@router.patch("/keys/{key}", response_model=Key, tags=["Meilisearch"])
async def update_key(
    key: str, update_key: KeyUpdate, client: AsyncClient = Depends(meilisearch_client)
) -> Key:
    return await client.update_key(update_key)


@router.get("/stats", response_model=ClientStats, tags=["Meilisearch"])
async def get_stats(client: AsyncClient = Depends(meilisearch_client)) -> ClientStats:
    return await client.get_all_stats()


@router.get("/version", response_model=Version, tags=["Meilisearch"])
async def get_version(client: AsyncClient = Depends(meilisearch_client)) -> Version:
    return await client.get_version()
