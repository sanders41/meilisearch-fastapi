from __future__ import annotations

from async_search_client import Client
from async_search_client.models import SearchResults
from fastapi import APIRouter, Depends

from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.search_parameters import SearchParameters

router = APIRouter()


@router.post("/", response_model=SearchResults)
async def search(
    search_parameters: SearchParameters, config: MeiliSearchConfig = Depends(get_config)
) -> SearchResults:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(search_parameters.uid)

        return await index.search(
            search_parameters.query,
            search_parameters.offset,
            search_parameters.limit,
            search_parameters.filters,
            search_parameters.facet_filters,
            search_parameters.facets_distribution,
            search_parameters.attributes_to_retrieve,
            search_parameters.attributes_to_crop,
            search_parameters.crop_length,
            search_parameters.attributes_to_highlight,
            search_parameters.matches,
        )
