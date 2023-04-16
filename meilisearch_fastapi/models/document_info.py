from typing import Any, Dict, List, Optional

from camel_converter.pydantic_base import CamelBase


class DocumentDelete(CamelBase):
    uid: str
    document_ids: List[str]


class DocumentInfo(CamelBase):
    uid: str
    documents: List[Dict[str, Any]]
    primary_key: Optional[str] = None


class DocumentInfoAutoBatch(DocumentInfo):
    max_payload_size: Optional[int] = None


class DocumentInfoBatches(DocumentInfo):
    batch_size: int
