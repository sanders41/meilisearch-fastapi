import asyncio
import json
from pathlib import Path

import pytest
from fastapi import APIRouter, FastAPI
from httpx import AsyncClient
from meilisearch_python_async import Client
from meilisearch_python_async.task import wait_for_task

from meilisearch_fastapi._config import get_config
from meilisearch_fastapi.routes import (
    document_routes,
    index_routes,
    meilisearch_routes,
    search_routes,
    settings_routes,
)

ROOT_PATH = Path().absolute()
SMALL_MOVIES_PATH = ROOT_PATH / "tests" / "assets" / "small_movies.json"

MASTER_KEY = "masterKey"
MEILISEARCH_URL = "localhost:7700"
INDEX_UID = "indexUID"
INDEX_UID2 = "indexUID2"
INDEX_UID3 = "indexUID3"
INDEX_UID4 = "indexUID4"

INDEX_FIXTURE = [
    {"uid": INDEX_UID},
    {"uid": INDEX_UID2, "primary_key": "book_id"},
]


@pytest.fixture(autouse=True)
def env_vars(monkeypatch):
    monkeypatch.setenv("MEILI_HTTP_ADDR", MEILISEARCH_URL)
    monkeypatch.setenv("MEILI_MASTER_KEY", MASTER_KEY)
    yield
    monkeypatch.delenv("MEILI_HTTP_ADDR", raising=False)
    monkeypatch.delenv("MEILI_MASTER_KEY", raising=False)


@pytest.fixture
def meilisearch_url():
    return MEILISEARCH_URL


@pytest.fixture
def master_key():
    return MASTER_KEY


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
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
    api_router.include_router(settings_routes.router, prefix="/settings")

    app.include_router(api_router)

    async with AsyncClient(app=app, base_url="http://test/", follow_redirects=True) as ac:
        yield ac


@pytest.fixture
@pytest.mark.asyncio
async def raw_client():
    async with Client(MEILISEARCH_URL, MASTER_KEY) as client:
        yield client


@pytest.mark.asyncio
@pytest.fixture(autouse=True)
async def clear_indexes(test_client):
    """Auto-clears the indexes after each test function run.
    Makes all the test functions independent.
    """

    yield
    async with Client(f"http://{MEILISEARCH_URL}", MASTER_KEY) as client:
        indexes = await client.get_indexes()
        if indexes:
            for index in indexes:
                response = await client.index(index.uid).delete()
                await wait_for_task(client.http_client, response.uid)


@pytest.fixture(autouse=True)
def clear_config_cache():
    yield
    get_config.cache_clear()


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
async def empty_index():
    async with Client(f"http://{MEILISEARCH_URL}", MASTER_KEY) as client:
        index = await client.create_index(uid=INDEX_UID)
        yield INDEX_UID, index


@pytest.fixture(scope="session")
def small_movies():
    """Runs once per session. Provides the content of small_movies.json"""

    with open(SMALL_MOVIES_PATH, "r") as movie_file:
        yield json.loads(movie_file.read())


@pytest.mark.asyncio
@pytest.fixture
async def index_with_documents(empty_index, small_movies):
    uid, index = empty_index
    response = await index.add_documents(small_movies)
    await wait_for_task(index.http_client, response.uid)

    yield uid, index


@pytest.mark.asyncio
@pytest.fixture
async def indexes_sample():
    async with Client(f"http://{MEILISEARCH_URL}", MASTER_KEY) as client:
        indexes = []
        for index_args in INDEX_FIXTURE:
            index = await client.create_index(**index_args)
            indexes.append(index)
        yield indexes
