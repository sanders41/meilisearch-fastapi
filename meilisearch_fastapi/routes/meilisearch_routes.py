from typing import List

from fastapi import APIRouter, Depends, HTTPException
from meilisearch_python_async import Client
from meilisearch_python_async.errors import InvalidRestriction
from meilisearch_python_async.models.client import ClientStats, Key, KeyCreate, KeyUpdate
from meilisearch_python_async.models.health import Health
from meilisearch_python_async.models.version import Version

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi.models.tenant_token import TenantToken, TenantTokenSettings

router = APIRouter()


@router.post("/generate-tenant-token", response_model=TenantToken, tags=["MeiliSearch"])
async def generate_tenant_token(
    tenant_token_settings: TenantTokenSettings, client: Client = Depends(meilisearch_client)
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


@router.get("/health", response_model=Health, tags=["MeiliSearch"])
async def get_health(client: Client = Depends(meilisearch_client)) -> Health:
    return await client.health()


@router.post("/keys", response_model=Key, tags=["MeiliSearch"])
async def create_key(key: KeyCreate, client: Client = Depends(meilisearch_client)) -> Key:
    return await client.create_key(key)


@router.delete("/keys/{key}", status_code=204, tags=["MeiliSearch"])
async def delete_key(key: str, client: Client = Depends(meilisearch_client)) -> int:
    return await client.delete_key(key)


@router.get("/keys", response_model=List[Key], tags=["MeiliSearch"])
async def get_keys(client: Client = Depends(meilisearch_client)) -> List[Key]:
    return await client.get_keys()


@router.get("/keys/{key}", response_model=Key, tags=["MeiliSearch"])
async def get_key(key: str, client: Client = Depends(meilisearch_client)) -> Key:
    return await client.get_key(key)


@router.patch("/keys/{key}", response_model=Key, tags=["MeiliSearch"])
async def update_key(
    key: str, update_key: KeyUpdate, client: Client = Depends(meilisearch_client)
) -> Key:
    return await client.update_key(update_key)


@router.get("/stats", response_model=ClientStats, tags=["MeiliSearch"])
async def get_stats(client: Client = Depends(meilisearch_client)) -> ClientStats:
    return await client.get_all_stats()


@router.get("/version", response_model=Version, tags=["MeiliSearch"])
async def get_version(client: Client = Depends(meilisearch_client)) -> Version:
    return await client.get_version()
