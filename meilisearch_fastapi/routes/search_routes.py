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
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(search_parameters.uid)

        return await index.search(
            query=search_parameters.query,
            offset=search_parameters.offset,
            limit=search_parameters.limit,
            filters=search_parameters.filters,
            facet_filters=search_parameters.facet_filters,
            facets_distribution=search_parameters.facets_distribution,
            attributes_to_retrieve=search_parameters.attributes_to_retrieve,
            attributes_to_crop=search_parameters.attributes_to_crop,
            crop_length=search_parameters.crop_length,
            attributes_to_highlight=search_parameters.attributes_to_highlight,
            matches=search_parameters.matches,
        )
