from __future__ import annotations

from async_search_client import Client
from async_search_client.models import UpdateId
from fastapi import APIRouter, Depends, HTTPException

from meilisearch_fastapi._config import MeiliSearchConfig, get_config
from meilisearch_fastapi.models.document_info import DocumentDelete, DocumentInfo

router = APIRouter()


@router.post("/", response_model=UpdateId)
async def add_documents(
    document_info: DocumentInfo, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(document_info.uid)

        return await index.add_documents(document_info.documents, document_info.primary_key)


@router.delete("/delete/{uid}", response_model=UpdateId)
async def delete_all_documents(
    uid: str, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)

        return await index.delete_all_documents()


@router.delete("/{uid}/{document_id}", response_model=UpdateId)
async def delete_document(
    uid: str, document_id: str, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)

        return await index.delete_document(document_id)


@router.post("/delete", response_model=UpdateId)
async def delete_documents(
    documents: DocumentDelete, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(documents.uid)

        return await index.delete_documents(documents.document_ids)


@router.get("/{uid}/{document_id}", response_model=dict)
async def get_document(
    uid: str, document_id: str, config: MeiliSearchConfig = Depends(get_config)
) -> dict:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)

        return await index.get_document(document_id)


@router.get("/{uid}", response_model=list[dict])
async def get_documents(uid: str, config: MeiliSearchConfig = Depends(get_config)) -> list[dict]:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(uid)
        documents = await index.get_documents()

        if documents is None:
            raise HTTPException(204, "No documents found")

        return documents


@router.put("/", response_model=UpdateId)
async def update_documents(
    document_info: DocumentInfo, config: MeiliSearchConfig = Depends(get_config)
) -> UpdateId:
    async with Client(url=config.url, api_key=config.api_key) as client:
        index = client.index(document_info.uid)

        return await index.update_documents(document_info.documents, document_info.primary_key)
