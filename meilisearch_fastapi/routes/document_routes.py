from typing import List, Optional

from fastapi import APIRouter, Depends
from meilisearch_python_sdk import AsyncClient
from meilisearch_python_sdk.models.documents import DocumentsInfo
from meilisearch_python_sdk.models.task import TaskInfo

from meilisearch_fastapi._client import meilisearch_client
from meilisearch_fastapi.models.document_info import (
    DocumentDelete,
    DocumentInfo,
    DocumentInfoBatches,
)

router = APIRouter()


@router.post("/", response_model=TaskInfo, status_code=202, tags=["Meilisearch Documents"])
async def add_documents(
    document_info: DocumentInfo,
    client: AsyncClient = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(document_info.uid)

    return await index.add_documents(document_info.documents, document_info.primary_key)


@router.post(
    "/batches", response_model=List[TaskInfo], status_code=202, tags=["Meilisearch Documents"]
)
async def add_documents_in_batches(
    document_info: DocumentInfoBatches, client: AsyncClient = Depends(meilisearch_client)
) -> List[TaskInfo]:
    index = client.index(document_info.uid)

    return await index.add_documents_in_batches(
        document_info.documents,
        batch_size=document_info.batch_size,
        primary_key=document_info.primary_key,
    )


@router.delete("/{uid}", response_model=TaskInfo, status_code=202, tags=["Meilisearch Documents"])
async def delete_all_documents(
    uid: str, client: AsyncClient = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(uid)

    return await index.delete_all_documents()


@router.delete(
    "/{uid}/{document_id}",
    response_model=TaskInfo,
    status_code=202,
    tags=["Meilisearch Documents"],
)
async def delete_document(
    uid: str, document_id: str, client: AsyncClient = Depends(meilisearch_client)
) -> TaskInfo:
    index = client.index(uid)

    return await index.delete_document(document_id)


@router.post("/delete", response_model=TaskInfo, status_code=202, tags=["Meilisearch Documents"])
async def delete_documents(
    documents: DocumentDelete,
    client: AsyncClient = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(documents.uid)

    return await index.delete_documents(documents.document_ids)


@router.get("/{uid}/{document_id}", response_model=dict, tags=["Meilisearch Documents"])
async def get_document(
    uid: str,
    document_id: str,
    client: AsyncClient = Depends(meilisearch_client),
) -> dict:
    index = client.index(uid)

    return await index.get_document(document_id)


@router.get("/{uid}", response_model=DocumentsInfo, tags=["Meilisearch Documents"])
async def get_documents(
    uid: str,
    limit: int = 20,
    offset: int = 0,
    fields: Optional[List[str]] = None,
    client: AsyncClient = Depends(meilisearch_client),
) -> DocumentsInfo:
    index = client.index(uid)

    documents = await index.get_documents(
        offset=offset,
        limit=limit,
        fields=fields,
    )

    return documents


@router.put("/", response_model=TaskInfo, status_code=202, tags=["Meilisearch Documents"])
async def update_documents(
    document_info: DocumentInfo,
    client: AsyncClient = Depends(meilisearch_client),
) -> TaskInfo:
    index = client.index(document_info.uid)

    return await index.update_documents(document_info.documents, document_info.primary_key)


@router.put(
    "/batches", response_model=List[TaskInfo], status_code=202, tags=["Meilisearch Documents"]
)
async def update_documents_in_batches(
    document_info: DocumentInfoBatches,
    client: AsyncClient = Depends(meilisearch_client),
) -> List[TaskInfo]:
    index = client.index(document_info.uid)

    return await index.update_documents_in_batches(
        document_info.documents,
        batch_size=document_info.batch_size,
        primary_key=document_info.primary_key,
    )
