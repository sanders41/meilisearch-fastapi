from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field, ValidationError, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class MeilisearchConfig(BaseSettings):
    MEILI_HTTP_ADDR: str
    MEILI_HTTPS_URL: bool = False
    MEILISEARCH_URL: str = "http://localhost:7700"
    MEILISEARCH_API_KEY: str | None = Field(None, validation_alias="MEILI_MASTER_KEY")
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    @model_validator(mode="before")
    def set_url(cls, values: dict[str, Any]) -> dict[str, Any]:
        if not values.get("MEILI_HTTP_ADDR"):
            raise ValidationError("A MEILI_HTTP_ADDR value is required", MeilisearchConfig)

        https = False

        if (
            values.get("MEILI_HTTPS_URL") is True
            or values.get("MEILI_HTTPS_URL", "").lower() == "true"
        ):
            https = True

        if https:
            values["MEILISEARCH_URL"] = f"https://{values.get('MEILI_HTTP_ADDR')}"
            return values

        values["MEILISEARCH_URL"] = f"http://{values.get('MEILI_HTTP_ADDR')}"
        return values


@lru_cache(maxsize=1)
def get_config() -> MeilisearchConfig:
    return MeilisearchConfig()  # type: ignore[call-arg]
