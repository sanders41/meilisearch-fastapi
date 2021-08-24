from __future__ import annotations

from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from meilisearch_python_async import Client
from meilisearch_python_async.models import UpdateId

from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.document_info import (
    DocumentDelete,
    DocumentInfo,
    DocumentInfoAutoBatch,
    DocumentInfoBatches,
)

router = APIRouter()


@router.post("/", response_model=UpdateId, status_code=202)
async def add_documents(
    document_info: DocumentInfo, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(document_info.uid)

        return await index.add_documents(document_info.documents, document_info.primary_key)


@router.post("/auto-batch", response_model=List[UpdateId], status_code=202)
async def add_documents_auto_batch(
    document_info: DocumentInfoAutoBatch, config: MeiliSearchConfig = Depends(get_config)
) -> list[UpdateId]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(document_info.uid)

        if document_info.max_payload_size:
            return await index.add_documents_auto_batch(
                document_info.documents,
                max_payload_size=document_info.max_payload_size,
                primary_key=document_info.primary_key,
            )

        return await index.add_documents_auto_batch(
            document_info.documents, primary_key=document_info.primary_key
        )


@router.post("/batches", response_model=List[UpdateId], status_code=202)
async def add_documents_in_batches(
    document_info: DocumentInfoBatches, config: MeiliSearchConfig = Depends(get_config)
) -> list[UpdateId]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(document_info.uid)

        return await index.add_documents_in_batches(
            document_info.documents,
            batch_size=document_info.batch_size,
            primary_key=document_info.primary_key,
        )


@router.delete("/{uid}", response_model=UpdateId, status_code=202)
async def delete_all_documents(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.delete_all_documents()


@router.delete("/{uid}/{document_id}", response_model=UpdateId, status_code=202)
async def delete_document(
    uid: str, document_id: str, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.delete_document(document_id)


@router.post("/delete", response_model=UpdateId, status_code=202)
async def delete_documents(
    documents: DocumentDelete, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(documents.uid)

        return await index.delete_documents(documents.document_ids)


@router.get("/{uid}/{document_id}", response_model=dict)
async def get_document(
    uid: str, document_id: str, config: MeiliSearchConfig = Depends(get_config)
) -> dict:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        return await index.get_document(document_id)


@router.get("/{uid}", response_model=List[Dict])
async def get_documents(
    uid: str,
    limit: int = 20,
    offset: int = 0,
    attributes_to_retrieve: str | None = None,
    config: MeiliSearchConfig = Depends(get_config),
) -> list[dict]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(uid)

        documents = await index.get_documents(
            offset=offset,
            limit=limit,
            attributes_to_retrieve=attributes_to_retrieve,
        )

        if documents is None:
            raise HTTPException(404, "No documents found")

        return documents


@router.put("/", response_model=UpdateId, status_code=202)
async def update_documents(
    document_info: DocumentInfo, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(document_info.uid)

        return await index.update_documents(document_info.documents, document_info.primary_key)


@router.put("/auto-batch", response_model=List[UpdateId], status_code=202)
async def update_documents_auto_batch(
    document_info: DocumentInfoAutoBatch, config: MeiliSearchConfig = Depends(get_config)
) -> list[UpdateId]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(document_info.uid)

        if document_info.max_payload_size:
            return await index.update_documents_auto_batch(
                document_info.documents,
                max_payload_size=document_info.max_payload_size,
                primary_key=document_info.primary_key,
            )

        return await index.update_documents_auto_batch(
            document_info.documents, primary_key=document_info.primary_key
        )


@router.put("/batches", response_model=List[UpdateId], status_code=202)
async def update_documents_in_batches(
    document_info: DocumentInfoBatches, config: MeiliSearchConfig = Depends(get_config)
) -> list[UpdateId]:
    async with Client(url=config.meilisearch_url, api_key=config.meilisearch_api_key) as client:
        index = client.index(document_info.uid)

        return await index.update_documents_in_batches(
            document_info.documents,
            batch_size=document_info.batch_size,
            primary_key=document_info.primary_key,
        )
