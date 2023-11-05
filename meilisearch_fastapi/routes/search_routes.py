from fastapi import APIRouter, Depends
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.search import SearchResults

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi.models.search_parameters import SearchParameters

router = APIRouter()


@router.post("/", response_model=SearchResults, tags=["Meilisearch Search"])
async def search(
    search_parameters: SearchParameters, client: AsyncClient = Depends(meilisearch_client)
) -> SearchResults:
    index = client.index(search_parameters.uid)

    return await index.search(
        query=search_parameters.query,
        offset=search_parameters.offset,
        limit=search_parameters.limit,
        filter=search_parameters.filter,
        facets=search_parameters.facets,
        attributes_to_retrieve=search_parameters.attributes_to_retrieve,
        attributes_to_crop=search_parameters.attributes_to_crop,
        sort=search_parameters.sort,
        crop_length=search_parameters.crop_length,
        attributes_to_highlight=search_parameters.attributes_to_highlight,
        show_matches_position=search_parameters.show_matches_position,
        highlight_pre_tag=search_parameters.highlight_pre_tag,
        highlight_post_tag=search_parameters.highlight_post_tag,
        crop_marker=search_parameters.crop_marker,
        matching_strategy=search_parameters.matching_strategy,
        hits_per_page=search_parameters.hits_per_page,
        page=search_parameters.page,
    )
