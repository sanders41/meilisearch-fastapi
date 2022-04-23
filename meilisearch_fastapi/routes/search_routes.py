from fastapi import APIRouter, Depends
from meilisearch_python_async import Client
from meilisearch_python_async.models.search import SearchResults

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi.models.search_parameters import SearchParameters

router = APIRouter()


@router.post("/", response_model=SearchResults, tags=["MeiliSearch Search"])
async def search(
    search_parameters: SearchParameters, client: Client = Depends(meilisearch_client)
) -> SearchResults:
    index = client.index(search_parameters.uid)

    return await index.search(
        query=search_parameters.query,
        offset=search_parameters.offset,
        limit=search_parameters.limit,
        filter=search_parameters.filter,
        facets_distribution=search_parameters.facets_distribution,
        attributes_to_retrieve=search_parameters.attributes_to_retrieve,
        attributes_to_crop=search_parameters.attributes_to_crop,
        sort=search_parameters.sort,
        crop_length=search_parameters.crop_length,
        attributes_to_highlight=search_parameters.attributes_to_highlight,
        matches=search_parameters.matches,
        highlight_pre_tag=search_parameters.highlight_pre_tag,
        highlight_post_tag=search_parameters.highlight_post_tag,
        crop_marker=search_parameters.crop_marker,
    )
