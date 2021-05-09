from __future__ import annotations

from async_search_client import Client
from async_search_client.models import ClientStats, Keys, Version  # Health,
from fastapi import APIRouter, Depends

from meilisearch_fastapi._config import MeiliSearchConfig, get_config

router = APIRouter()


# @router.get("/health", resopnse_model=Health)
# async def get_health(config: MeiliSearchConfig = Depends(get_config)) -> Health:
#    async with Client(url=config.url, api_key=config.api_key) as client:
#        return await client.health()


@router.get("/keys", response_model=Keys)
async def get_keys(config: MeiliSearchConfig = Depends(get_config)) -> Keys:
    async with Client(url=config.url, api_key=config.api_key) as client:
        return await client.get_keys()


@router.get("/stats", response_model=ClientStats)
async def get_stats(config: MeiliSearchConfig = Depends(get_config)) -> ClientStats:
    async with Client(url=config.url, api_key=config.api_key) as client:
        return await client.get_all_stats()


@router.get("/version", response_model=Version)
async def get_version(config: MeiliSearchConfig = Depends(get_config)) -> Version:
    async with Client(url=config.url, api_key=config.api_key) as client:
        return await client.get_version()
