from __future__ import annotations

from datetime import datetime
from typing import Any

from camel_converter.pydantic_base import CamelBase
from meilisearch_python_sdk.models.client import Key


class TenantToken(CamelBase):
    tenant_token: str


class TenantTokenSettings(CamelBase):
    search_rules: dict[str, Any] | list[str]
    api_key: Key
    expires_at: datetime | None = None
