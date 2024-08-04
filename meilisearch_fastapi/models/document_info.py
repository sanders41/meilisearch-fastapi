from __future__ import annotations

from typing import Any

from camel_converter.pydantic_base import CamelBase


class DocumentDelete(CamelBase):
    uid: str
    document_ids: list[str]


class DocumentInfo(CamelBase):
    uid: str
    documents: list[dict[str, Any]]
    primary_key: str | None = None


class DocumentInfoAutoBatch(DocumentInfo):
    max_payload_size: int | None = None


class DocumentInfoBatches(DocumentInfo):
    batch_size: int
