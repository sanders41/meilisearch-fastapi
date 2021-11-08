from __future__ import annotations

from fastapi import APIRouter, Depends
from meilisearch_python_async import Client
from meilisearch_python_async.models import ClientStats, Health, Keys, Version

from meilisearch_fastapi._config import MeiliSearchConfig, get_config

router = APIRouter()


@router.get("/health", response_model=Health, tags=["MeiliSearch"])
async def get_health(config: MeiliSearchConfig = Depends(get_config)) -> Health:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.health()


@router.get("/keys", response_model=Keys, tags=["MeiliSearch"])
async def get_keys(config: MeiliSearchConfig = Depends(get_config)) -> Keys:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_keys()


@router.get("/stats", response_model=ClientStats, tags=["MeiliSearch"])
async def get_stats(config: MeiliSearchConfig = Depends(get_config)) -> ClientStats:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_all_stats()


@router.get("/version", response_model=Version, tags=["MeiliSearch"])
async def get_version(config: MeiliSearchConfig = Depends(get_config)) -> Version:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        return await client.get_version()
