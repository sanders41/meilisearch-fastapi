from typing import AsyncGenerator

from meilisearch_python_async import Client

from meilisearch_fastapi._config import get_config


async def meilisearch_client() -> AsyncGenerator[Client, None]:
    config = get_config()
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        yield client
