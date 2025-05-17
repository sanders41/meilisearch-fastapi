from collections.abc import AsyncGenerator

from meilisearch_python_sdk import AsyncClient

from meilisearch_fastapi._config import get_config


async def meilisearch_client() -> AsyncGenerator[AsyncClient, None]:
    config = get_config()
    async with AsyncClient(
        url=config.MEILISEARCH_URL, api_key=config.MEILISEARCH_API_KEY
    ) as client:
        yield client
