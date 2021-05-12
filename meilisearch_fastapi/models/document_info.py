from typing import Dict, List, Optional

from camel_converter.pydantic_base import CamelBase


class DocumentDelete(CamelBase):
    uid: str
    document_ids: List[str]


class DocumentInfo(CamelBase):
    uid: str
    documents: List[Dict]
    primary_key: Optional[str] = None
