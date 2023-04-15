from functools import lru_cache
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, root_validator
from pydantic.error_wrappers import ValidationError


class MeilisearchConfig(BaseSettings):
    meili_http_addr: str = Field(..., env="MEILI_HTTP_ADDR")
    meili_https_url: bool = Field(False, env="MEILI_HTTPS_URL")
    meilisearch_url: str = "http://localhost:7700"
    meilisearch_api_key: Optional[str] = Field(None, env="MEILI_MASTER_KEY")

    @root_validator
    def set_url(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if not values.get("meili_http_addr"):
            raise ValidationError("A MEILI_HTTP_ADDR value is required", MeilisearchConfig)

        if values["meili_https_url"]:
            values["meilisearch_url"] = f"https://{values['meili_http_addr']}"
            return values

        values["meilisearh_url"] = f"http://{values['meili_http_addr']}"
        return values

    class Config:
        env_file = ".env"


@lru_cache(maxsize=1)
def get_config() -> MeilisearchConfig:
    return MeilisearchConfig()  # type: ignore[call-arg]
