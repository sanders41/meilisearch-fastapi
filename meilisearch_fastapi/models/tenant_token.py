from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from camel_converter.pydantic_base import CamelBase
from meilisearch_python_sdk.models.client import Key


class TenantToken(CamelBase):
    tenant_token: str


class TenantTokenSettings(CamelBase):
    search_rules: Union[Dict[str, Any], List[str]]
    api_key: Key
    expires_at: Optional[datetime] = None
