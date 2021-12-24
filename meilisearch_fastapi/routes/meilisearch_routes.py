from typing import List

from fastapi import APIRouter, Depends
from meilisearch_python_async import Client
from meilisearch_python_async.models.client import ClientStats, Key, KeyCreate, KeyUpdate
from meilisearch_python_async.models.health import Health
from meilisearch_python_async.models.version import Version

from meilisearch_fastapi._config import MeiliSearchConfig, get_config

router = APIRouter()


@router.get("/health", response_model=Health, tags=["MeiliSearch"])
async def get_health(config: MeiliSearchConfig = Depends(get_config)) -> Health:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.health()


@router.post("/keys", response_model=Key, tags=["MeiliSearch"])
async def create_key(key: KeyCreate, config: MeiliSearchConfig = Depends(get_config)) -> Key:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.create_key(key)


@router.delete("/keys/{key}", status_code=204, tags=["MeiliSearch"])
async def delete_key(key: str, config: MeiliSearchConfig = Depends(get_config)) -> int:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.delete_key(key)


@router.get("/keys", response_model=List[Key], tags=["MeiliSearch"])
async def get_keys(config: MeiliSearchConfig = Depends(get_config)) -> List[Key]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_keys()


@router.get("/keys/{key}", response_model=Key, tags=["MeiliSearch"])
async def get_key(key: str, config: MeiliSearchConfig = Depends(get_config)) -> Key:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_key(key)


@router.patch("/keys/{key}", response_model=Key, tags=["MeiliSearch"])
async def update_key(
    key: str, update_key: KeyUpdate, config: MeiliSearchConfig = Depends(get_config)
) -> Key:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.update_key(update_key)


@router.get("/stats", response_model=ClientStats, tags=["MeiliSearch"])
async def get_stats(config: MeiliSearchConfig = Depends(get_config)) -> ClientStats:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_all_stats()


@router.get("/version", response_model=Version, tags=["MeiliSearch"])
async def get_version(config: MeiliSearchConfig = Depends(get_config)) -> Version:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_version()
