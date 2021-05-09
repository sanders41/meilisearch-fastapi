import asyncio

import pytest
from async_search_client import Client
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient

from meilisearch_fastapi.routes import (
    document_routes,
    index_routes,
    meilisearch_routes,
    search_routes,
    setting_routes,
)

MASTER_KEY = "masterKey"
MEILISEARCH_URL = "http://localhost:7700"
INDEX_UID = "indexUID"
INDEX_UID2 = "indexUID2"
INDEX_UID3 = "indexUID3"
INDEX_UID4 = "indexUID4"

INDEX_FIXTURE = [
    {"uid": INDEX_UID},
    {"uid": INDEX_UID2, "primary_key": "book_id"},
]


@pytest.fixture(scope="session")
def env_vars(monkeypatch):
    monkeypatch.setenv("MEILISEARCH_URL", MEILISEARCH_URL)
    monkeypatch.setenv("MEILISEARCH_API_KEY", MASTER_KEY)
    yield


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_client():
    app = FastAPI()
    api_router = APIRouter()
    api_router.include_router(document_routes.router, prefix="/documents")
    api_router.include_router(index_routes.router, prefix="/indexes")
    api_router.include_router(meilisearch_routes.router, prefix="/meilisearch")
    api_router.include_router(search_routes.router, prefix="/search")
    api_router.include_router(setting_routes.router, prefix="/settings")

    app.include_router(api_router)

    async with AsyncClient(app=app, base_url="http://test/") as ac:
        yield ac


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def clear_indexes(test_client):
    """
    Auto-clears the indexes after each test function run.
    Makes all the test functions independent.
    """
    yield
    async with Client(MEILISEARCH_URL, MASTER_KEY) as client:
        indexes = await client.get_indexes()
        if indexes:
            for index in indexes:
                await client.index(index.uid).delete()


@pytest.fixture
def index_uid():
    return INDEX_UID


@pytest.fixture
def index_uid2():
    return INDEX_UID2


@pytest.fixture
def index_uid3():
    return INDEX_UID3


@pytest.fixture
def index_uid4():
    return INDEX_UID4


@pytest.mark.asyncio
@pytest.fixture
async def indexes_sample(test_client):
    async with Client(MEILISEARCH_URL, MASTER_KEY) as client:
        indexes = []
        for index_args in INDEX_FIXTURE:
            index = await client.create_index(**index_args)
            indexes.append(index)

    yield indexes
