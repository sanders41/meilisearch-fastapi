from typing import AsyncGenerator

from meilisearch_python_sdk import AsyncClient

from meilisearch_fastapi._config import get_config


async def meilisearch_client() -> AsyncGenerator[AsyncClient, None]:
    config = get_config()
    async with AsyncClient(
        url=config.meilisearch_url, api_key=config.meilisearch_api_key
    ) as client:
        yield client
