from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MeilisearchConfig(BaseSettings):
    meili_http_addr: str
    meili_https_url: bool = False
    meilisearch_url: str = "http://localhost:7700"
    meilisearch_api_key: Optional[str] = Field(None, validation_alias="MEILI_MASTER_KEY")
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    @model_validator(mode="before")
    def set_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("meili_http_addr"):
            raise ValidationError("A MEILI_HTTP_ADDR value is required", MeilisearchConfig)

        https = False

        if (
            values.get("meili_https_url") is True
            or values.get("meili_https_url", "").lower() == "true"
        ):
            https = True

        if https:
            values["meilisearch_url"] = f"https://{values.get('meili_http_addr')}"
            return values

        values["meilisearh_url"] = f"http://{values.get('meili_http_addr')}"
        return values


@lru_cache(maxsize=1)
def get_config() -> MeilisearchConfig:
    return MeilisearchConfig()  # type: ignore[call-arg]
